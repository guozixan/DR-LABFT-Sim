class QueueController:
    def __init__(self, low_threshold=0.5, high_threshold=0.7, 
                min_batch=80, max_batch=150):
        self.queue = deque()
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.min_batch = min_batch
        self.max_batch = max_batch
        self.current_batch_size = max_batch
        self.overflow_count = 0
    
    def add_request(self, request):
        if self.is_overloaded():
            self.overflow_count += 1
            return False
            
        self.queue.append(request)
        return True
    
    def get_batch(self):
        if len(self.queue) < self.current_batch_size:
            return list(self.queue)
        
        batch = []
        for _ in range(self.current_batch_size):
            batch.append(self.queue.popleft())
        return batch
    
    def adjust_batch_size(self, system_load):
        if system_load < self.low_threshold:
            # 轻载状态 - 扩大批处理
            self.current_batch_size = min(
                self.current_batch_size + 10, 
                self.max_batch
            )
        elif system_load > self.high_threshold:
            # 重载状态 - 缩小批处理
            self.current_batch_size = max(
                self.current_batch_size - 15, 
                self.min_batch
            )
    
    def is_overloaded(self):
        return len(self.queue) > config.MAX_QUEUE_SIZE
    
    def get_queue_status(self):
        return {
            'size': len(self.queue),
            'batch_size': self.current_batch_size,
            'overflow': self.overflow_count
        }