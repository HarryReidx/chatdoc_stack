"""
简单几何计算 - shapely的替代实现
Author: AI Assistant
Date: 2025-07-29
"""
import math
from typing import List, Tuple

class Point:
    """简单的点类"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, other):
        """计算到另一个点的距离"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class LineString:
    """简单的线段类"""
    
    def __init__(self, coordinates):
        """
        初始化线段
        :param coordinates: 坐标列表，如 [(x1, y1), (x2, y2), ...]
        """
        self.coordinates = coordinates
        self.coords = coordinates  # 兼容shapely接口
    
    def length(self):
        """计算线段总长度"""
        total_length = 0
        for i in range(len(self.coordinates) - 1):
            p1 = Point(*self.coordinates[i])
            p2 = Point(*self.coordinates[i + 1])
            total_length += p1.distance(p2)
        return total_length
    
    def distance(self, point):
        """计算点到线段的最短距离"""
        if isinstance(point, Point):
            point = (point.x, point.y)
        
        min_distance = float('inf')
        
        # 计算点到每个线段的距离
        for i in range(len(self.coordinates) - 1):
            p1 = self.coordinates[i]
            p2 = self.coordinates[i + 1]
            
            # 计算点到线段的距离
            dist = self._point_to_line_distance(point, p1, p2)
            min_distance = min(min_distance, dist)
        
        return min_distance
    
    def _point_to_line_distance(self, point, line_start, line_end):
        """计算点到线段的距离"""
        px, py = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # 线段长度的平方
        line_length_sq = (x2 - x1)**2 + (y2 - y1)**2
        
        if line_length_sq == 0:
            # 线段退化为点
            return math.sqrt((px - x1)**2 + (py - y1)**2)
        
        # 计算投影参数
        t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_sq))
        
        # 投影点
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        
        # 返回距离
        return math.sqrt((px - proj_x)**2 + (py - proj_y)**2)
    
    def intersects(self, other):
        """检查是否与另一个几何对象相交"""
        # 简单实现，可以根据需要扩展
        return False
    
    def __repr__(self):
        return f"LineString({self.coordinates})"

class Polygon:
    """简单的多边形类"""
    
    def __init__(self, coordinates):
        """
        初始化多边形
        :param coordinates: 坐标列表，如 [(x1, y1), (x2, y2), ...]
        """
        self.coordinates = coordinates
        self.exterior = LineString(coordinates)
    
    def area(self):
        """计算多边形面积（使用鞋带公式）"""
        n = len(self.coordinates)
        if n < 3:
            return 0
        
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += self.coordinates[i][0] * self.coordinates[j][1]
            area -= self.coordinates[j][0] * self.coordinates[i][1]
        
        return abs(area) / 2
    
    def contains(self, point):
        """检查点是否在多边形内（射线法）"""
        if isinstance(point, Point):
            x, y = point.x, point.y
        else:
            x, y = point
        
        n = len(self.coordinates)
        inside = False
        
        p1x, p1y = self.coordinates[0]
        for i in range(1, n + 1):
            p2x, p2y = self.coordinates[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def __repr__(self):
        return f"Polygon({self.coordinates})"

# 兼容性函数
def point(x, y):
    """创建点"""
    return Point(x, y)

def linestring(coordinates):
    """创建线段"""
    return LineString(coordinates)

def polygon(coordinates):
    """创建多边形"""
    return Polygon(coordinates)
