import asyncio
from database import init_db, AsyncSessionLocal, User, ChatSession, ChatMessage
from sqlalchemy import select

async def test_db():
    print("🚀 Initializing Database...")
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # 1. Create User
        print("👤 Creating Test User...")
        test_email = "test@wellora.com"
        res = await db.execute(select(User).where(User.email == test_email))
        user = res.scalar_one_or_none()
        
        if not user:
            user = User(name="Test User", email=test_email, password="password123")
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"✅ User created: {user.id}")
        else:
            print(f"ℹ️ User already exists: {user.id}")

        # 2. Create Session
        print("📂 Creating Chat Session...")
        session_id = "test-session-uuid"
        res = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
        session = res.scalar_one_or_none()
        
        if not session:
            session = ChatSession(id=session_id, user_id=user.id, title="Test Heart Health")
            db.add(session)
            await db.commit()
            await db.refresh(session)
            print(f"✅ Session created: {session.id}")
        else:
            print(f"ℹ️ Session already exists: {session.id}")

        # 3. Add Messages
        print("💬 Adding Test Messages...")
        msg1 = ChatMessage(session_id=session_id, role="user", content="Hello, my heart hurts.")
        msg2 = ChatMessage(session_id=session_id, role="assistant", content="I'm sorry to hear that. Please seek medical help.")
        db.add_all([msg1, msg2])
        await db.commit()
        print("✅ Messages added.")

        # 4. Verify Retrieval
        print("🔍 Verifying Retrieval...")
        res = await db.execute(select(ChatMessage).where(ChatMessage.session_id == session_id))
        msgs = res.scalars().all()
        print(f"📝 Found {len(msgs)} messages in session.")
        for m in msgs:
            print(f"   [{m.role}]: {m.content[:30]}...")

    print("\n🎉 Database Verification Complete!")

if __name__ == "__main__":
    asyncio.run(test_db())
