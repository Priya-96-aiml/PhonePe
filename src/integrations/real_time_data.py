"""
Real-time data streaming and processing capabilities.
Supports WebSockets, Kafka, and other streaming sources.
"""

import asyncio
import websockets
import json
import logging
from typing import Dict, List, Optional, Any, Callable
import pandas as pd
from datetime import datetime, timedelta
import threading
import queue
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class StreamConfig:
    """Configuration for data streams."""
    name: str
    source_type: str  # websocket, kafka, api_polling
    endpoint: str
    update_interval: int = 60  # seconds
    buffer_size: int = 1000
    auto_start: bool = True

class RealTimeDataStream:
    """Real-time data streaming manager."""
    
    def __init__(self):
        self.streams = {}
        self.data_buffers = {}
        self.callbacks = {}
        self.running_streams = set()
        
    def register_stream(self, config: StreamConfig, callback: Callable = None):
        """Register a new data stream."""
        self.streams[config.name] = config
        self.data_buffers[config.name] = queue.Queue(maxsize=config.buffer_size)
        
        if callback:
            self.callbacks[config.name] = callback
            
        logger.info(f"Registered stream: {config.name}")
        
        if config.auto_start:
            self.start_stream(config.name)
    
    def start_stream(self, stream_name: str):
        """Start a data stream."""
        if stream_name not in self.streams:
            raise ValueError(f"Stream {stream_name} not registered")
            
        if stream_name in self.running_streams:
            logger.warning(f"Stream {stream_name} already running")
            return
            
        config = self.streams[stream_name]
        
        if config.source_type == 'websocket':
            thread = threading.Thread(
                target=self._websocket_stream,
                args=(stream_name, config),
                daemon=True
            )
        elif config.source_type == 'api_polling':
            thread = threading.Thread(
                target=self._api_polling_stream,
                args=(stream_name, config),
                daemon=True
            )
        else:
            raise ValueError(f"Unsupported stream type: {config.source_type}")
            
        thread.start()
        self.running_streams.add(stream_name)
        logger.info(f"Started stream: {stream_name}")
    
    def stop_stream(self, stream_name: str):
        """Stop a data stream."""
        if stream_name in self.running_streams:
            self.running_streams.remove(stream_name)
            logger.info(f"Stopped stream: {stream_name}")
    
    def get_latest_data(self, stream_name: str, count: int = 100) -> List[Dict]:
        """Get latest data from stream buffer."""
        if stream_name not in self.data_buffers:
            raise ValueError(f"Stream {stream_name} not found")
            
        buffer = self.data_buffers[stream_name]
        data = []
        
        # Get up to 'count' items from queue
        for _ in range(min(count, buffer.qsize())):
            try:
                data.append(buffer.get_nowait())
            except queue.Empty:
                break
                
        return data
    
    def get_stream_dataframe(self, stream_name: str, count: int = 100) -> pd.DataFrame:
        """Get stream data as DataFrame."""
        data = self.get_latest_data(stream_name, count)
        return pd.DataFrame(data) if data else pd.DataFrame()
    
    def _websocket_stream(self, stream_name: str, config: StreamConfig):
        """WebSocket streaming implementation."""
        async def websocket_handler():
            try:
                async with websockets.connect(config.endpoint) as websocket:
                    logger.info(f"WebSocket connected: {stream_name}")
                    
                    while stream_name in self.running_streams:
                        try:
                            message = await asyncio.wait_for(
                                websocket.recv(), 
                                timeout=30
                            )
                            
                            data = json.loads(message)
                            data['timestamp'] = datetime.now().isoformat()
                            
                            # Add to buffer
                            buffer = self.data_buffers[stream_name]
                            if buffer.full():
                                buffer.get()  # Remove oldest item
                            buffer.put(data)
                            
                            # Call callback if registered
                            if stream_name in self.callbacks:
                                self.callbacks[stream_name](data)
                                
                        except asyncio.TimeoutError:
                            logger.warning(f"WebSocket timeout: {stream_name}")
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error in {stream_name}: {e}")
                            
            except Exception as e:
                logger.error(f"WebSocket error in {stream_name}: {e}")
            finally:
                if stream_name in self.running_streams:
                    self.running_streams.remove(stream_name)
        
        # Run the async function
        asyncio.run(websocket_handler())
    
    def _api_polling_stream(self, stream_name: str, config: StreamConfig):
        """API polling streaming implementation."""
        import requests
        
        while stream_name in self.running_streams:
            try:
                response = requests.get(config.endpoint, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                data['timestamp'] = datetime.now().isoformat()
                
                # Add to buffer
                buffer = self.data_buffers[stream_name]
                if buffer.full():
                    buffer.get()  # Remove oldest item
                buffer.put(data)
                
                # Call callback if registered
                if stream_name in self.callbacks:
                    self.callbacks[stream_name](data)
                    
                time.sleep(config.update_interval)
                
            except Exception as e:
                logger.error(f"API polling error in {stream_name}: {e}")
                time.sleep(config.update_interval)

class MarketDataStream(RealTimeDataStream):
    """Specialized stream for financial market data."""
    
    def __init__(self):
        super().__init__()
        
    def add_stock_stream(self, symbol: str, api_key: str):
        """Add real-time stock price stream."""
        config = StreamConfig(
            name=f"stock_{symbol}",
            source_type='websocket',
            endpoint=f"wss://ws.finnhub.io?token={api_key}",
            update_interval=1
        )
        
        def stock_callback(data):
            """Process stock data."""
            if 'data' in data:
                for trade in data['data']:
                    trade['symbol'] = symbol
                    trade['processed_at'] = datetime.now().isoformat()
        
        self.register_stream(config, stock_callback)
    
    def add_crypto_stream(self, symbol: str):
        """Add cryptocurrency price stream."""
        config = StreamConfig(
            name=f"crypto_{symbol}",
            source_type='websocket',
            endpoint=f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker",
            update_interval=1
        )
        
        self.register_stream(config)

class IoTDataStream(RealTimeDataStream):
    """Specialized stream for IoT sensor data."""
    
    def __init__(self):
        super().__init__()
        
    def add_sensor_stream(self, sensor_id: str, mqtt_broker: str, topic: str):
        """Add IoT sensor data stream."""
        # This would integrate with MQTT broker
        config = StreamConfig(
            name=f"sensor_{sensor_id}",
            source_type='api_polling',  # Simplified for demo
            endpoint=f"http://{mqtt_broker}/api/sensors/{sensor_id}",
            update_interval=10
        )
        
        def sensor_callback(data):
            """Process sensor data."""
            data['sensor_id'] = sensor_id
            data['processed_at'] = datetime.now().isoformat()
        
        self.register_stream(config, sensor_callback)

class SocialMediaStream(RealTimeDataStream):
    """Stream for social media data."""
    
    def __init__(self):
        super().__init__()
        
    def add_twitter_stream(self, bearer_token: str, keywords: List[str]):
        """Add Twitter stream for keywords."""
        # Twitter API v2 streaming
        config = StreamConfig(
            name="twitter_stream",
            source_type='api_polling',  # Simplified
            endpoint="https://api.twitter.com/2/tweets/search/stream",
            update_interval=30
        )
        
        def twitter_callback(data):
            """Process Twitter data."""
            data['keywords'] = keywords
            data['processed_at'] = datetime.now().isoformat()
        
        self.register_stream(config, twitter_callback)

# Example usage and integration
class StreamingAnalytics:
    """Analytics engine for streaming data."""
    
    def __init__(self, stream_manager: RealTimeDataStream):
        self.stream_manager = stream_manager
        self.analytics_results = {}
        
    def calculate_moving_average(self, stream_name: str, column: str, window: int = 10) -> float:
        """Calculate moving average from stream data."""
        df = self.stream_manager.get_stream_dataframe(stream_name, window)
        
        if df.empty or column not in df.columns:
            return None
            
        return df[column].mean()
    
    def detect_anomalies(self, stream_name: str, column: str, threshold: float = 2.0) -> List[Dict]:
        """Detect anomalies in streaming data."""
        df = self.stream_manager.get_stream_dataframe(stream_name, 100)
        
        if df.empty or column not in df.columns:
            return []
            
        mean = df[column].mean()
        std = df[column].std()
        
        anomalies = []
        for _, row in df.iterrows():
            z_score = abs((row[column] - mean) / std) if std > 0 else 0
            if z_score > threshold:
                anomalies.append({
                    'timestamp': row.get('timestamp'),
                    'value': row[column],
                    'z_score': z_score,
                    'type': 'anomaly'
                })
                
        return anomalies
    
    def generate_alerts(self, stream_name: str, conditions: Dict[str, Any]) -> List[Dict]:
        """Generate alerts based on conditions."""
        df = self.stream_manager.get_stream_dataframe(stream_name, 10)
        
        if df.empty:
            return []
            
        alerts = []
        latest_row = df.iloc[-1]
        
        for column, condition in conditions.items():
            if column in latest_row:
                value = latest_row[column]
                
                if condition['type'] == 'threshold':
                    if value > condition['max'] or value < condition['min']:
                        alerts.append({
                            'stream': stream_name,
                            'column': column,
                            'value': value,
                            'condition': condition,
                            'timestamp': latest_row.get('timestamp'),
                            'alert_type': 'threshold_breach'
                        })
                        
        return alerts