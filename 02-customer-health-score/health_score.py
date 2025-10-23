"""
Health Score Calculator Module
Calculates customer health scores based on usage metrics
"""

import numpy as np


class HealthScoreCalculator:
    """Calculator for customer health scores"""

    def __init__(self):
        """Initialize with default weights"""
        self.weights = {
            'login_frequency': 0.30,
            'feature_usage': 0.25,
            'support_tickets': 0.20,
            'days_since_last_login': 0.15,
            'contract_value': 0.10
        }

    def normalize_score(self, value, min_val, max_val, invert=False):
        """
        Normalize a value to 0-100 scale

        Args:
            value: Raw value
            min_val: Minimum expected value
            max_val: Maximum expected value
            invert: If True, lower values get higher scores
        """
        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0, min(1, normalized))  # Clamp to [0, 1]

        if invert:
            normalized = 1 - normalized

        return normalized * 100

    def calculate_health_score(
        self,
        login_frequency,
        feature_usage,
        support_tickets,
        days_since_last_login,
        contract_value
    ):
        """
        Calculate overall health score

        Args:
            login_frequency: Logins per month
            feature_usage: Number of features used (0-100)
            support_tickets: Number of support tickets
            days_since_last_login: Days since last login
            contract_value: Annual contract value

        Returns:
            Health score (0-100)
        """
        # Normalize each metric
        login_score = self.normalize_score(login_frequency, 0, 30, invert=False)
        feature_score = self.normalize_score(feature_usage, 0, 100, invert=False)
        support_score = self.normalize_score(support_tickets, 0, 20, invert=True)
        recency_score = self.normalize_score(days_since_last_login, 0, 90, invert=True)
        value_score = self.normalize_score(contract_value, 0, 100000, invert=False)

        # Calculate weighted score
        health_score = (
            login_score * self.weights['login_frequency'] +
            feature_score * self.weights['feature_usage'] +
            support_score * self.weights['support_tickets'] +
            recency_score * self.weights['days_since_last_login'] +
            value_score * self.weights['contract_value']
        )

        return round(health_score, 2)

    def categorize_risk(self, health_score):
        """
        Categorize customer risk based on health score

        Args:
            health_score: Health score (0-100)

        Returns:
            Risk category string
        """
        if health_score >= 70:
            return "Healthy"
        elif health_score >= 40:
            return "At Risk"
        else:
            return "High Risk"

    def predict_churn_probability(self, health_score):
        """
        Predict churn probability based on health score

        Args:
            health_score: Health score (0-100)

        Returns:
            Churn probability (0-1)
        """
        # Sigmoid-like function for churn probability
        # High health score = low churn probability
        churn_prob = 1 / (1 + np.exp((health_score - 50) / 10))
        return round(churn_prob, 4)

    def get_recommendations(
        self,
        health_score,
        login_frequency,
        support_tickets,
        days_since_last_login
    ):
        """
        Generate recommendations based on customer metrics

        Args:
            health_score: Overall health score
            login_frequency: Logins per month
            support_tickets: Number of support tickets
            days_since_last_login: Days since last login

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if health_score < 40:
            recommendations.append("🚨 HIGH PRIORITY: Schedule immediate check-in call with customer success team")

        if login_frequency < 5:
            recommendations.append("📧 Low engagement detected. Send re-engagement campaign highlighting key features")

        if support_tickets > 10:
            recommendations.append("🎯 High support volume. Investigate common issues and provide proactive solutions")

        if days_since_last_login > 30:
            recommendations.append("⏰ Customer hasn't logged in recently. Send personalized re-activation email")

        if days_since_last_login > 60:
            recommendations.append("📞 Consider phone outreach to understand barriers to usage")

        if health_score >= 70:
            recommendations.append("✅ Healthy customer! Consider upsell opportunities or request testimonial")

        if not recommendations:
            recommendations.append("✓ Customer is stable. Continue regular monitoring")

        return recommendations
