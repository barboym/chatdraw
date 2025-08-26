### TODO

- [ ] Add `uv` installation to the Dockerfiles
- [ ] Develop a scoring service
- [ ] Correct frontend div alignment
- [ ] Add chat history
- [ ] Improve the SVG generation: RAG, different model?
- [ ] Store the conversations 
- [ ] Session management

Session management by GPT-4.1:

## Step-by-Step Guide: Making the FastAPI App Stateful

### 1. **Session Management Strategy**
Decide how to identify users and persist their chat state:
- **Option A:** Use HTTP cookies with a session ID.
- **Option B:** Use authentication tokens (JWT, etc.).
- **Option C:** Use a unique user ID passed in each request (e.g., in headers or body).

**Recommendation:** For chat, cookies or a user/session ID in the request is simplest.

---

### 2. **State Storage Backend**
Choose where to store session/chat state:
- **In-memory:** Use a Python dict (simple, but not scalable or persistent).
- **Database:** Use PostgreSQL, Redis, or similar for persistence and scalability.

**Recommendation:** Start with in-memory for prototyping, then move to Redis/PostgreSQL for production.

---

### 3. **Backend Changes**
#### a. **Session/State Store**
- Create a global dict or connect to a database to store user sessions and chat contexts.

#### b. **User Identification**
- On each request, extract the user/session ID (from cookie, header, or body).
- If new, initialize a session; if existing, load the session state.

#### c. **Stateful Chat Handling**
- Store and update the chat context and message history for each user/session.
- When a message is received, retrieve the user's context, process the message, update the context, and save it back.

#### d. **Endpoints**
- Modify the root endpoint to accept a user/session ID.
- Optionally, add endpoints for session management (start, end, reset).

---

### 4. **Frontend Changes**
- Send the user/session ID with each request (in headers, cookies, or body).
- No longer need to persist chat context on the frontend.

---

### 5. **Persistence (Optional)**
- For production, replace the in-memory store with a persistent backend (e.g., Redis or PostgreSQL).

---

## Example Flow

1. **User opens chat:**  
   - Frontend requests a new session/user ID from backend or generates one.
2. **User sends message:**  
   - Frontend sends message + session/user ID to backend.
3. **Backend:**  
   - Looks up session state by ID, processes message, updates state, returns response.
4. **Frontend:**  
   - Displays response, does not need to track context.

---

## Summary Table

| Step                | Backend Change                | Frontend Change                |
|---------------------|------------------------------|-------------------------------|
| Session management  | Add session ID extraction     | Send session/user ID           |
| State storage       | Store context per session     | Remove context tracking        |
| Chat handling       | Use session context           | No change to message sending   |
| Persistence         | Use DB/Redis for state        | No change                     |

