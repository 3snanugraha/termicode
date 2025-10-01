"""Session manager for conversation persistence"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class SessionManager:
    """Manage conversation sessions with local storage"""

    def __init__(self, sessions_dir: str = ".termicode_sessions"):
        self.sessions_dir = sessions_dir
        self.current_session_file: Optional[str] = None

        # Create sessions directory if not exists
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)

    def create_session(self, session_name: Optional[str] = None) -> str:
        """Create new session and return session file path"""
        if session_name is None:
            # Auto-generate session name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_name = f"session_{timestamp}"

        session_file = os.path.join(self.sessions_dir, f"{session_name}.json")
        self.current_session_file = session_file

        # Initialize empty session
        self._save_session([])
        return session_file

    def load_session(self, session_name: str) -> List[Dict[str, str]]:
        """Load conversation history from session file"""
        session_file = os.path.join(self.sessions_dir, f"{session_name}.json")

        if not os.path.exists(session_file):
            raise FileNotFoundError(f"Session '{session_name}' not found")

        self.current_session_file = session_file

        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('history', [])

    def save_message(self, conversation_history: List[Dict[str, str]]):
        """Save current conversation to session file"""
        if self.current_session_file is None:
            self.create_session()

        self._save_session(conversation_history)

    def _save_session(self, conversation_history: List[Dict[str, str]]):
        """Internal method to save session data"""
        session_data = {
            'created_at': datetime.now().isoformat(),
            'message_count': len(conversation_history),
            'history': conversation_history
        }

        with open(self.current_session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all available sessions"""
        sessions = []

        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.sessions_dir, filename)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        sessions.append({
                            'name': filename.replace('.json', ''),
                            'created_at': data.get('created_at'),
                            'message_count': data.get('message_count', 0)
                        })
                except Exception:
                    continue

        # Sort by created_at descending
        sessions.sort(key=lambda x: x['created_at'], reverse=True)
        return sessions

    def delete_session(self, session_name: str):
        """Delete a session file"""
        session_file = os.path.join(self.sessions_dir, f"{session_name}.json")

        if os.path.exists(session_file):
            os.remove(session_file)

    def get_session_info(self, session_name: str) -> Dict[str, Any]:
        """Get session metadata"""
        session_file = os.path.join(self.sessions_dir, f"{session_name}.json")

        if not os.path.exists(session_file):
            raise FileNotFoundError(f"Session '{session_name}' not found")

        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                'name': session_name,
                'created_at': data.get('created_at'),
                'message_count': data.get('message_count', 0),
                'size_kb': os.path.getsize(session_file) / 1024
            }
