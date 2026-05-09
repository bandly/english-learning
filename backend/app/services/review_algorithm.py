"""
艾宾浩斯遗忘曲线复习算法
基于 SM-2 (SuperMemo 2) 算法改进

评分等级说明：
0: 完全忘记
1: 记得一点，但很费力
2: 记得，但有些犹豫
3: 记得，比较轻松
4: 记得很清楚
5: 完美记忆
"""

from datetime import datetime, timedelta
from typing import Tuple
import math


class EbbinghausAlgorithm:
    """基于SM-2算法的艾宾浩斯复习算法"""

    def __init__(self):
        self.default_ease_factor = 2.5
        self.min_ease_factor = 1.3

    def calculate_next_review(
        self,
        quality: int,  # 用户评分 0-5
        review_count: int,  # 已复习次数
        ease_factor: float,  # 当前难度因子
        last_interval: int  # 上次间隔天数
    ) -> Tuple[datetime, int, float]:
        """
        计算下次复习时间和参数

        返回: (下次复习时间, 间隔天数, 新难度因子)
        """
        # 1. 更新难度因子 (SM-2公式)
        new_ef = self._calculate_ease_factor(quality, ease_factor)

        # 2. 计算间隔
        if quality < 3:
            # 如果评分低于3，重新开始学习
            interval = 1
            new_review_count = 0
            new_ef = self.default_ease_factor  # 重置难度因子
        else:
            # 根据复习次数计算间隔
            if review_count == 0:
                interval = 1
            elif review_count == 1:
                interval = 2
            else:
                interval = math.ceil(last_interval * new_ef)

            new_review_count = review_count + 1

        # 3. 计算下次复习时间
        next_review_date = datetime.now() + timedelta(days=interval)

        # 4. 判断状态
        status = self._get_status(new_review_count, interval)

        return next_review_date, interval, new_ef, status, new_review_count

    def _calculate_ease_factor(self, quality: int, ease_factor: float) -> float:
        """
        根据评分更新难度因子
        SM-2公式: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        """
        new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        return max(self.min_ease_factor, new_ef)

    def _get_status(self, review_count: int, interval: int) -> str:
        """判断学习状态"""
        if review_count == 0:
            return "learning"
        elif interval >= 30:
            return "mastered"
        else:
            return "review"

    def get_initial_review_schedule(self) -> Tuple[datetime, int, int, float, str]:
        """
        获取新单词的初始复习计划
        返回: (首次复习时间, 间隔天数, 复习次数, 难度因子, 状态)
        """
        return (
            datetime.now() + timedelta(days=1),
            1,
            0,
            self.default_ease_factor,
            "learning"
        )

    def calculate_retention_rate(self, days_since_last_review: int, ease_factor: float) -> float:
        """
        计算记忆保持率（基于艾宾浩斯遗忘曲线公式）
        R = e^(-t/S) where S is stability
        """
        stability = ease_factor * 10
        retention = math.exp(-days_since_last_review / stability)
        return max(0, min(1, retention))


# 使用示例
class ReviewService:
    def __init__(self):
        self.algorithm = EbbinghausAlgorithm()

    def create_initial_schedule(self, user_id: int, item_type: str) -> dict:
        """为新项目创建初始复习计划"""
        next_review, interval, count, ef, status = self.algorithm.get_initial_review_schedule()

        return {
            "user_id": user_id,
            "item_type": item_type,
            "next_review_date": next_review,
            "interval_days": interval,
            "review_count": count,
            "ease_factor": ef,
            "status": status
        }

    def update_schedule(
        self,
        current_schedule: dict,
        quality: int
    ) -> dict:
        """根据用户评分更新复习计划"""
        next_review, interval, new_ef, status, new_count = self.algorithm.calculate_next_review(
            quality=quality,
            review_count=current_schedule["review_count"],
            ease_factor=current_schedule["ease_factor"],
            last_interval=current_schedule["interval_days"]
        )

        return {
            "next_review_date": next_review,
            "interval_days": interval,
            "review_count": new_count,
            "ease_factor": new_ef,
            "status": status,
            "last_review_date": datetime.now()
        }