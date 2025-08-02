"""
Data seeding script for LifeSwap platform
Run this to populate the database with sample life experiences
"""
import json
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.user import User
from models.experience import LifeExperience, Scenario, ScenarioChoice
from models.reflection import Badge, Challenge
from utils.auth import get_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample badges
        badges = [
            {
                "name": "First Steps",
                "description": "Complete your first life experience",
                "category": "exploration",
                "criteria_type": "experience_count",
                "criteria_value": 1,
                "rarity": "common",
                "points_value": 10
            },
            {
                "name": "Global Explorer",
                "description": "Experience stories from 5 different countries",
                "category": "diversity",
                "criteria_type": "region_diversity",
                "criteria_value": 5,
                "rarity": "rare",
                "points_value": 50
            },
            {
                "name": "Empathy Champion",
                "description": "Earn 1000 empathy points",
                "category": "empathy",
                "criteria_type": "empathy_points",
                "criteria_value": 1000,
                "rarity": "epic",
                "points_value": 100
            }
        ]
        
        for badge_data in badges:
            badge = Badge(**badge_data)
            db.add(badge)
        
        # Create sample admin user
        admin_user = User(
            email="admin@lifeswap.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_admin=True,
            empathy_points=500,
            total_experiences=5,
            badges=json.dumps([])
        )
        db.add(admin_user)
        
        # Create sample life experiences
        experiences_data = [
            {
                "title": "Day in the Life: Syrian Refugee Teen",
                "description": "Experience the daily challenges and hopes of Amal, a 16-year-old Syrian refugee living in Jordan.",
                "category": "refugee",
                "region": "Middle East",
                "culture": "Syrian",
                "difficulty_level": "intermediate",
                "estimated_duration": 25,
                "cultural_context": "Syria has been in civil war since 2011, displacing millions of people. Many refugees live in camps or urban areas in neighboring countries.",
                "learning_objectives": json.dumps([
                    "Understand the daily challenges faced by refugee youth",
                    "Learn about resilience and hope in difficult circumstances",
                    "Explore the importance of education for displaced populations"
                ]),
                "tags": json.dumps(["refugee", "education", "middle-east", "youth"]),
                "is_published": True,
                "is_featured": True
            },
            {
                "title": "Living with Visual Impairment in Mumbai",
                "description": "Navigate the bustling streets and social challenges as Priya, a university student who lost her sight at age 12.",
                "category": "disability",
                "region": "South Asia",
                "culture": "Indian",
                "difficulty_level": "beginner",
                "estimated_duration": 20,
                "cultural_context": "India has over 8 million people with visual impairments. Access to education and employment can be challenging.",
                "learning_objectives": json.dumps([
                    "Experience daily navigation challenges",
                    "Understand accessibility barriers",
                    "Learn about adaptive technologies and techniques"
                ]),
                "tags": json.dumps(["disability", "accessibility", "education", "india"]),
                "is_published": True,
                "is_featured": False
            },
            {
                "title": "Single Mother in Rural Guatemala",
                "description": "Make difficult decisions about work, family, and education as Maria, raising three children alone.",
                "category": "poverty",
                "region": "Central America",
                "culture": "Guatemalan",
                "difficulty_level": "advanced",
                "estimated_duration": 30,
                "cultural_context": "Rural Guatemala faces high poverty rates, with limited access to education and healthcare.",
                "learning_objectives": json.dumps([
                    "Understand the intersection of gender and poverty",
                    "Explore difficult choices between immediate needs and long-term goals",
                    "Learn about community support systems"
                ]),
                "tags": json.dumps(["poverty", "single-parent", "rural", "guatemala"]),
                "is_published": True,
                "is_featured": True
            },
            {
                "title": "Elderly Care Worker in Japan",
                "description": "Experience the emotional and physical demands of caring for aging populations as Hiroshi.",
                "category": "profession",
                "region": "East Asia",
                "culture": "Japanese",
                "difficulty_level": "intermediate",
                "estimated_duration": 22,
                "cultural_context": "Japan has one of the world's most rapidly aging populations, creating unique caregiving challenges.",
                "learning_objectives": json.dumps([
                    "Understand the challenges of an aging society",
                    "Experience the emotional labor of caregiving",
                    "Learn about dignity and respect in elder care"
                ]),
                "tags": json.dumps(["elderly-care", "aging", "healthcare", "japan"]),
                "is_published": True,
                "is_featured": False
            },
            {
                "title": "LGBTQ+ Youth in Conservative Town",
                "description": "Navigate identity, family relationships, and community acceptance as Alex, a transgender teenager.",
                "category": "identity",
                "region": "North America",
                "culture": "American",
                "difficulty_level": "advanced",
                "estimated_duration": 28,
                "cultural_context": "LGBTQ+ youth often face unique challenges in conservative communities, including family rejection and discrimination.",
                "learning_objectives": json.dumps([
                    "Understand the challenges of gender identity exploration",
                    "Experience the impact of community acceptance/rejection",
                    "Learn about resilience and self-advocacy"
                ]),
                "tags": json.dumps(["lgbtq", "identity", "youth", "family"]),
                "is_published": True,
                "is_featured": False
            }
        ]
        
        experiences = []
        for exp_data in experiences_data:
            experience = LifeExperience(**exp_data)
            db.add(experience)
            db.flush()  # Get the ID
            experiences.append(experience)
        
        # Create sample scenarios for the first experience (Syrian Refugee Teen)
        exp1 = experiences[0]
        
        # Opening scenario
        scenario1 = Scenario(
            experience_id=exp1.id,
            title="Morning in the Camp",
            content="You wake up in the small tent you share with your family. The sound of children playing and adults talking fills the air. You have an important decision to make about your day.",
            scenario_type="decision",
            order_index=1,
            points_awarded=5
        )
        db.add(scenario1)
        db.flush()
        
        # Choices for scenario 1
        choice1_1 = ScenarioChoice(
            scenario_id=scenario1.id,
            choice_text="Go to the educational center for classes",
            consequence_text="You choose education, showing determination for your future despite difficult circumstances.",
            points_impact=10,
            choice_type="empathetic",
            order_index=1
        )
        choice1_2 = ScenarioChoice(
            scenario_id=scenario1.id,
            choice_text="Help your mother with daily chores",
            consequence_text="You prioritize family support, showing the difficult balance between personal goals and family responsibilities.",
            points_impact=8,
            choice_type="practical",
            order_index=2
        )
        choice1_3 = ScenarioChoice(
            scenario_id=scenario1.id,
            choice_text="Try to find work to help with family income",
            consequence_text="You focus on immediate survival needs, illustrating the tough economic realities refugees face.",
            points_impact=6,
            choice_type="practical",
            order_index=3
        )
        
        db.add_all([choice1_1, choice1_2, choice1_3])
        
        # Second scenario
        scenario2 = Scenario(
            experience_id=exp1.id,
            title="A Difficult Conversation",
            content="Your family is discussing the possibility of returning to Syria versus trying to relocate to Europe. Everyone has different opinions and fears.",
            scenario_type="decision",
            order_index=2,
            points_awarded=10
        )
        db.add(scenario2)
        db.flush()
        
        # Choices for scenario 2
        choice2_1 = ScenarioChoice(
            scenario_id=scenario2.id,
            choice_text="Advocate for staying and building a life in Jordan",
            consequence_text="You choose stability and gradual integration, valuing the community you've built.",
            points_impact=12,
            choice_type="empathetic",
            order_index=1
        )
        choice2_2 = ScenarioChoice(
            scenario_id=scenario2.id,
            choice_text="Support the idea of trying to reach Europe",
            consequence_text="You're willing to take risks for better opportunities, understanding the dangers involved.",
            points_impact=8,
            choice_type="risky",
            order_index=2
        )
        
        db.add_all([choice2_1, choice2_2])
        
        # Final scenario
        scenario3 = Scenario(
            experience_id=exp1.id,
            title="Looking Toward Tomorrow",
            content="As you reflect on your experiences, you think about what you want your future to look like and how your experiences have shaped your perspective on resilience and hope.",
            scenario_type="reflection",
            order_index=3,
            points_awarded=15
        )
        db.add(scenario3)
        
        # Create a sample challenge
        challenge = Challenge(
            title="Diversity Explorer",
            description="Complete experiences from 3 different regions this week",
            challenge_type="weekly",
            target_count=3,
            points_reward=50,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7),
            is_active=True
        )
        db.add(challenge)
        
        db.commit()
        print("✅ Sample data created successfully!")
        print("📊 Created:")
        print("  - 5 life experiences")
        print("  - 3 badges")
        print("  - 1 admin user (admin@lifeswap.com / admin123)")
        print("  - Sample scenarios for Syrian Refugee experience")
        print("  - 1 weekly challenge")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Creating sample data for LifeSwap...")
    create_sample_data()