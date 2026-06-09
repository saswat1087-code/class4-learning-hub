"""
Data Manager Module
Handles all data persistence, progress tracking, achievements, and user statistics
"""

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict

class DataManager:
    """Manages all user data, progress tracking, and achievements"""
    
    def __init__(self):
        """Initialize data manager with session state defaults"""
        self.data_file = "user_progress.json"
        self.achievements_config = self.load_achievements_config()
        self.init_session_state()
    
    def load_achievements_config(self) -> Dict:
        """Load achievements/badges configuration"""
        return {
            "badges": {
                "First Steps": {
                    "description": "Earn your first 50 points",
                    "requirement": 50,
                    "type": "points",
                    "icon": "🌟",
                    "color": "#FFD700"
                },
                "Quiz Starter": {
                    "description": "Complete your first quiz",
                    "requirement": 1,
                    "type": "quizzes",
                    "icon": "📝",
                    "color": "#4CAF50"
                },
                "Knowledge Seeker": {
                    "description": "Complete 3 quizzes",
                    "requirement": 3,
                    "type": "quizzes",
                    "icon": "📚",
                    "color": "#2196F3"
                },
                "Chapter Master": {
                    "description": "Complete 3 chapters",
                    "requirement": 3,
                    "type": "chapters",
                    "icon": "👑",
                    "color": "#FF9800"
                },
                "Perfect Score": {
                    "description": "Get 100% on any quiz",
                    "requirement": 100,
                    "type": "perfect_score",
                    "icon": "⭐",
                    "color": "#FFC107"
                },
                "100 Points Club": {
                    "description": "Earn 100 total points",
                    "requirement": 100,
                    "type": "points",
                    "icon": "💯",
                    "color": "#9C27B0"
                },
                "Star Learner": {
                    "description": "Earn 500 total points",
                    "requirement": 500,
                    "type": "points",
                    "icon": "⭐",
                    "color": "#FFD700"
                },
                "Streak Champion": {
                    "description": "Study for 7 days in a row",
                    "requirement": 7,
                    "type": "streak",
                    "icon": "🔥",
                    "color": "#FF5722"
                },
                "Quiz Champion": {
                    "description": "Complete 10 quizzes",
                    "requirement": 10,
                    "type": "quizzes",
                    "icon": "🏆",
                    "color": "#FFD700"
                },
                "Learning Legend": {
                    "description": "Earn 1000 total points",
                    "requirement": 1000,
                    "type": "points",
                    "icon": "👑",
                    "color": "#E91E63"
                },
                "Math Wizard": {
                    "description": "Score 90%+ in 3 math quizzes",
                    "requirement": 3,
                    "type": "subject_mastery",
                    "subject": "Mathematics",
                    "icon": "🧮",
                    "color": "#3F51B5"
                },
                "Science Explorer": {
                    "description": "Score 90%+ in 3 science quizzes",
                    "requirement": 3,
                    "type": "subject_mastery",
                    "subject": "Science",
                    "icon": "🔬",
                    "color": "#4CAF50"
                },
                "Computer Pro": {
                    "description": "Score 90%+ in 3 computer quizzes",
                    "requirement": 3,
                    "type": "subject_mastery",
                    "subject": "Computer Science",
                    "icon": "💻",
                    "color": "#00BCD4"
                },
                "English Star": {
                    "description": "Score 90%+ in 3 English quizzes",
                    "requirement": 3,
                    "type": "subject_mastery",
                    "subject": "English Literature",
                    "icon": "📖",
                    "color": "#9C27B0"
                },
                "Early Bird": {
                    "description": "Study before 9 AM",
                    "requirement": 5,
                    "type": "early_study",
                    "icon": "🌅",
                    "color": "#FF9800"
                },
                "Night Owl": {
                    "description": "Study after 8 PM",
                    "requirement": 5,
                    "type": "night_study",
                    "icon": "🦉",
                    "color": "#607D8B"
                },
                "Homework Hero": {
                    "description": "Complete 5 assignments",
                    "requirement": 5,
                    "type": "assignments",
                    "icon": "📋",
                    "color": "#8BC34A"
                },
                "Helping Hand": {
                    "description": "Help other students 10 times",
                    "requirement": 10,
                    "type": "helpful",
                    "icon": "🤝",
                    "color": "#FF4081"
                }
            },
            "levels": [
                {"level": 1, "points_required": 0, "title": "New Explorer"},
                {"level": 2, "points_required": 100, "title": "Curious Learner"},
                {"level": 3, "points_required": 250, "title": "Rising Star"},
                {"level": 4, "points_required": 500, "title": "Knowledge Builder"},
                {"level": 5, "points_required": 800, "title": "Smart Thinker"},
                {"level": 6, "points_required": 1200, "title": "Brilliant Mind"},
                {"level": 7, "points_required": 1700, "title": "Learning Master"},
                {"level": 8, "points_required": 2300, "title": "Genius Level"},
                {"level": 9, "points_required": 3000, "title": "Super Scholar"},
                {"level": 10, "points_required": 4000, "title": "Legendary Learner"}
            ]
        }
    
    def init_session_state(self):
        """Initialize all session state variables with defaults"""
        defaults = {
            # User profile
            'user_name': "Learner",
            'user_avatar': "👧",
            'user_grade': 4,
            'join_date': datetime.now().strftime("%Y-%m-%d"),
            
            # Progress tracking
            'points_earned': 0,
            'total_questions_answered': 0,
            'correct_answers': 0,
            'total_quiz_score': 0,
            'total_quizzes_taken': 0,
            
            # Streaks
            'current_streak': 0,
            'longest_streak': 0,
            'last_study_date': None,
            'study_days': [],
            
            # Completion tracking
            'completed_chapters': [],
            'completed_quizzes': [],
            'completed_assignments': [],
            'subject_progress': defaultdict(dict),
            
            # Quiz scores
            'quiz_scores': {},
            'subject_scores': defaultdict(list),
            'daily_scores': [],
            
            # Badges and achievements
            'badges': [],
            'badges_earned_date': {},
            'achievements_unlocked': [],
            
            # Study time tracking
            'total_study_time': 0,  # in minutes
            'daily_study_time': {},
            'current_session_start': None,
            
            # Helpful actions
            'helpful_count': 0,
            'questions_asked': 0,
            'ai_interactions': 0,
            
            # Learning preferences
            'favorite_subject': None,
            'learning_streak_notifications': True,
            'daily_goal': 50,  # points per day
            
            # Challenges
            'daily_challenge': None,
            'daily_challenge_completed': False,
            'weekly_challenge': None,
            'weekly_challenge_progress': 0
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
        
        # Update streak
        self.update_streak()
    
    def update_streak(self):
        """Update the study streak based on last activity"""
        today = datetime.now().date()
        
        if st.session_state.last_study_date:
            last_date = datetime.strptime(st.session_state.last_study_date, "%Y-%m-%d").date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Consecutive day
                st.session_state.current_streak += 1
                if st.session_state.current_streak > st.session_state.longest_streak:
                    st.session_state.longest_streak = st.session_state.current_streak
            elif days_diff > 1:
                # Streak broken
                st.session_state.current_streak = 1
            # else: same day, no change
        else:
            st.session_state.current_streak = 1
        
        # Add today to study days if not already
        today_str = today.strftime("%Y-%m-%d")
        if today_str not in st.session_state.study_days:
            st.session_state.study_days.append(today_str)
        
        st.session_state.last_study_date = today.strftime("%Y-%m-%d")
    
    def award_points(self, points: int, reason: str = "", category: str = "general") -> int:
        """
        Award points to the user and check for achievements
        
        Args:
            points: Number of points to award
            reason: Reason for awarding points
            category: Category of activity (quiz, chapter, help, etc.)
        
        Returns:
            Total points after addition
        """
        # Update points
        st.session_state.points_earned += points
        
        # Track category-specific points
        if category == "quiz":
            st.session_state.total_quiz_score += points
            st.session_state.total_quizzes_taken += 1
        elif category == "question":
            st.session_state.total_questions_answered += 1
            if "correct" in reason.lower():
                st.session_state.correct_answers += 1
        elif category == "helpful":
            st.session_state.helpful_count += 1
        elif category == "ai":
            st.session_state.ai_interactions += 1
        
        # Show notification
        if points > 0:
            st.toast(f"🎉 +{points} points! {reason}", icon="⭐")
        
        # Check for new badges/achievements
        new_badges = self.check_achievements()
        
        if new_badges:
            for badge in new_badges:
                st.balloons()
                st.success(f"🏆 Congratulations! You earned the '{badge}' badge! 🏆")
        
        # Check daily goal
        self.check_daily_goal()
        
        # Save progress
        self.save_progress()
        
        return st.session_state.points_earned
    
    def check_achievements(self) -> List[str]:
        """Check and award achievements/badges"""
        new_badges = []
        
        for badge_name, badge_config in self.achievements_config["badges"].items():
            # Skip if already earned
            if badge_name in st.session_state.badges:
                continue
            
            earned = False
            
            # Check based on badge type
            if badge_config["type"] == "points":
                if st.session_state.points_earned >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "quizzes":
                if len(st.session_state.completed_quizzes) >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "chapters":
                if len(st.session_state.completed_chapters) >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "perfect_score":
                # Check if any quiz has 100% score
                for score in st.session_state.quiz_scores.values():
                    if isinstance(score, dict) and score.get('percentage', 0) >= 100:
                        earned = True
                        break
                    elif isinstance(score, (int, float)) and score >= 100:
                        earned = True
                        break
            
            elif badge_config["type"] == "streak":
                if st.session_state.current_streak >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "subject_mastery":
                # Count high-scoring quizzes in specific subject
                subject = badge_config.get("subject")
                if subject:
                    high_scores = 0
                    for quiz_name, score in st.session_state.quiz_scores.items():
                        if subject.lower() in quiz_name.lower():
                            if isinstance(score, dict):
                                if score.get('percentage', 0) >= 90:
                                    high_scores += 1
                            elif isinstance(score, (int, float)) and score >= 90:
                                high_scores += 1
                    if high_scores >= badge_config["requirement"]:
                        earned = True
            
            elif badge_config["type"] == "early_study":
                # Count early morning study sessions
                early_sessions = sum(1 for date in st.session_state.study_days 
                                   if date.startswith("early"))
                if early_sessions >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "night_study":
                # Count evening study sessions
                night_sessions = sum(1 for date in st.session_state.study_days 
                                   if date.startswith("night"))
                if night_sessions >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "assignments":
                if len(st.session_state.completed_assignments) >= badge_config["requirement"]:
                    earned = True
            
            elif badge_config["type"] == "helpful":
                if st.session_state.helpful_count >= badge_config["requirement"]:
                    earned = True
            
            if earned:
                st.session_state.badges.append(badge_name)
                st.session_state.badges_earned_date[badge_name] = datetime.now().strftime("%Y-%m-%d")
                new_badges.append(badge_name)
        
        return new_badges
    
    def get_current_level(self) -> Dict:
        """Get current level information"""
        points = st.session_state.points_earned
        
        for i in range(len(self.achievements_config["levels"]) - 1, -1, -1):
            level_info = self.achievements_config["levels"][i]
            if points >= level_info["points_required"]:
                next_level = self.achievements_config["levels"][i + 1] if i + 1 < len(self.achievements_config["levels"]) else None
                points_to_next = next_level["points_required"] - points if next_level else 0
                
                return {
                    "level": level_info["level"],
                    "title": level_info["title"],
                    "points_required": level_info["points_required"],
                    "points_to_next": points_to_next,
                    "next_title": next_level["title"] if next_level else "Max Level"
                }
        
        return {"level": 1, "title": "New Explorer", "points_required": 0, "points_to_next": 100}
    
    def complete_chapter(self, chapter_name: str, subject: str) -> bool:
        """Mark a chapter as completed"""
        chapter_key = f"{subject}: {chapter_name}"
        
        if chapter_key not in st.session_state.completed_chapters:
            st.session_state.completed_chapters.append(chapter_key)
            
            # Award points for completing chapter
            self.award_points(50, f"for completing {chapter_name}!", category="chapter")
            
            # Track subject progress
            if subject not in st.session_state.subject_progress:
                st.session_state.subject_progress[subject] = {"completed": [], "scores": []}
            st.session_state.subject_progress[subject]["completed"].append(chapter_name)
            
            return True
        
        return False
    
    def save_quiz_score(self, subject: str, score: int, total: int, chapter: str = "") -> Dict:
        """
        Save a quiz score and return performance metrics
        
        Returns:
            Dictionary with performance metrics
        """
        percentage = (score / total) * 100 if total > 0 else 0
        quiz_name = f"{subject}_{chapter}" if chapter else subject
        
        # Save score
        st.session_state.quiz_scores[quiz_name] = {
            "score": score,
            "total": total,
            "percentage": percentage,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": subject,
            "chapter": chapter
        }
        
        # Add to completed quizzes
        st.session_state.completed_quizzes.append(quiz_name)
        
        # Track subject scores
        st.session_state.subject_scores[subject].append(percentage)
        
        # Award points based on performance
        points_earned = int(score * 10)  # 10 points per correct answer
        self.award_points(points_earned, f"for scoring {score}/{total} on {subject} quiz!", category="quiz")
        
        # Special bonus for perfect score
        if percentage == 100:
            self.award_points(50, "Perfect score bonus! 🌟", category="bonus")
        
        # Update daily score
        today = datetime.now().strftime("%Y-%m-%d")
        st.session_state.daily_scores.append({
            "date": today,
            "subject": subject,
            "score": percentage
        })
        
        return {
            "percentage": percentage,
            "points_earned": points_earned,
            "is_perfect": percentage == 100,
            "message": f"Great job! You scored {score}/{total} ({percentage:.0f}%)!"
        }
    
    def get_subject_mastery(self, subject: str) -> float:
        """Calculate mastery percentage for a subject"""
        scores = st.session_state.subject_scores.get(subject, [])
        if not scores:
            return 0.0
        
        average_score = sum(scores) / len(scores)
        return round(average_score, 1)
    
    def get_progress_report(self) -> Dict:
        """Generate comprehensive progress report"""
        level_info = self.get_current_level()
        
        # Calculate accuracy
        accuracy = 0
        if st.session_state.total_questions_answered > 0:
            accuracy = (st.session_state.correct_answers / st.session_state.total_questions_answered) * 100
        
        # Calculate study time this week
        week_study_time = 0
        today = datetime.now().date()
        for date_str, minutes in st.session_state.daily_study_time.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if (today - date_obj).days <= 7:
                    week_study_time += minutes
            except:
                pass
        
        report = {
            "user_name": st.session_state.user_name,
            "join_date": st.session_state.join_date,
            "current_level": level_info["level"],
            "level_title": level_info["title"],
            "total_points": st.session_state.points_earned,
            "points_to_next_level": level_info["points_to_next"],
            
            "study_stats": {
                "current_streak": st.session_state.current_streak,
                "longest_streak": st.session_state.longest_streak,
                "total_study_days": len(st.session_state.study_days),
                "total_study_time": st.session_state.total_study_time,
                "week_study_time": week_study_time
            },
            
            "quiz_stats": {
                "total_quizzes": len(st.session_state.completed_quizzes),
                "average_score": self.get_average_quiz_score(),
                "best_subject": self.get_best_subject(),
                "total_questions": st.session_state.total_questions_answered,
                "accuracy": round(accuracy, 1)
            },
            
            "completion_stats": {
                "chapters_completed": len(st.session_state.completed_chapters),
                "assignments_completed": len(st.session_state.completed_assignments),
                "badges_earned": len(st.session_state.badges)
            },
            
            "subject_mastery": {
                subject: self.get_subject_mastery(subject)
                for subject in ["Computer Science", "English Literature", "Mathematics", "Science"]
                if subject in st.session_state.subject_scores
            },
            
            "badges": st.session_state.badges,
            "recent_activity": self.get_recent_activity()
        }
        
        return report
    
    def get_average_quiz_score(self) -> float:
        """Calculate average quiz score percentage"""
        if not st.session_state.quiz_scores:
            return 0.0
        
        total_percentage = 0
        for score_data in st.session_state.quiz_scores.values():
            if isinstance(score_data, dict):
                total_percentage += score_data.get('percentage', 0)
            elif isinstance(score_data, (int, float)):
                total_percentage += score_data
        
        return round(total_percentage / len(st.session_state.quiz_scores), 1)
    
    def get_best_subject(self) -> str:
        """Determine the subject with highest average score"""
        best_subject = None
        best_score = 0
        
        for subject, scores in st.session_state.subject_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score > best_score:
                best_score = avg_score
                best_subject = subject
        
        return best_subject if best_subject else "None yet"
    
    def get_recent_activity(self, days: int = 7) -> List[Dict]:
        """Get recent activity for the last N days"""
        recent = []
        today = datetime.now().date()
        
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            # Get activities for this date
            day_activities = []
            
            # Check if studied on this day
            if date_str in st.session_state.study_days:
                day_activities.append("📚 Studied")
            
            # Check for quizzes on this day
            for quiz_name, score_data in st.session_state.quiz_scores.items():
                if isinstance(score_data, dict) and score_data.get('date', '').startswith(date_str):
                    day_activities.append(f"📝 Quiz: {score_data.get('percentage', 0):.0f}%")
            
            # Check for badges on this day
            for badge, badge_date in st.session_state.badges_earned_date.items():
                if badge_date == date_str:
                    day_activities.append(f"🏆 Earned: {badge}")
            
            if day_activities:
                recent.append({
                    "date": date_str,
                    "day_name": date.strftime("%A"),
                    "activities": day_activities
                })
        
        return recent
    
    def check_daily_goal(self):
        """Check if daily goal is met"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get today's points
        today_points = 0
        # This would need to track points per day - simplified version
        if st.session_state.points_earned >= st.session_state.daily_goal:
            if not st.session_state.daily_challenge_completed:
                st.session_state.daily_challenge_completed = True
                self.award_points(25, "Daily goal completed! 🎯", category="bonus")
                st.balloons()
                st.success(f"🎉 Amazing! You reached your daily goal of {st.session_state.daily_goal} points!")
    
    def save_progress(self):
        """Save user progress to local file"""
        try:
            # Prepare data to save
            save_data = {
                "user_name": st.session_state.user_name,
                "points_earned": st.session_state.points_earned,
                "completed_chapters": st.session_state.completed_chapters,
                "completed_quizzes": st.session_state.completed_quizzes,
                "quiz_scores": st.session_state.quiz_scores,
                "badges": st.session_state.badges,
                "current_streak": st.session_state.current_streak,
                "longest_streak": st.session_state.longest_streak,
                "study_days": st.session_state.study_days,
                "last_study_date": st.session_state.last_study_date,
                "total_study_time": st.session_state.total_study_time
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            # Silently fail - don't disrupt user experience
            pass
    
    def load_progress(self):
        """Load user progress from local file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    load_data = json.load(f)
                
                # Restore data
                for key, value in load_data.items():
                    if key in st.session_state:
                        st.session_state[key] = value
                
                return True
        except Exception:
            pass
        return False
    
    def reset_progress(self, confirmation: bool = False) -> bool:
        """Reset all user progress"""
        if confirmation:
            # Clear all progress data
            st.session_state.points_earned = 0
            st.session_state.completed_chapters = []
            st.session_state.completed_quizzes = []
            st.session_state.quiz_scores = {}
            st.session_state.badges = []
            st.session_state.current_streak = 0
            st.session_state.longest_streak = 0
            st.session_state.total_study_time = 0
            
            # Save empty progress
            self.save_progress()
            
            return True
        return False
    
    def add_study_time(self, minutes: int):
        """Add study time for the current session"""
        st.session_state.total_study_time += minutes
        
        today = datetime.now().strftime("%Y-%m-%d")
        if today in st.session_state.daily_study_time:
            st.session_state.daily_study_time[today] += minutes
        else:
            st.session_state.daily_study_time[today] = minutes
        
        # Award bonus for studying 30+ minutes
        if st.session_state.daily_study_time.get(today, 0) >= 30:
            if not hasattr(st.session_state, 'study_bonus_awarded_today'):
                self.award_points(10, "30-minute study bonus! 💪", category="bonus")
                st.session_state.study_bonus_awarded_today = True

# Create a singleton instance
@st.cache_resource
def get_data_manager():
    """Get or create the data manager instance"""
    return DataManager()

# Initialize the data manager
data_manager = get_data_manager()
