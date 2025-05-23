
### 🧠 Project Overview
The system comprises two main components

1. **Server Application**:
   - **MCP Server**:Utilizes the MCP framework to expose tools that the AI can invoke
   - **Express Server**:Handles HTTP requests and manages Server-Sent Events (SSE) for real-time communication
   - **Defined Tools**:
     - `addTwoNumbers`: Performs addition of two numbers.
     - `createPost`: Posts a status update to X using the Twitter API.

2. **Client Application**:
   - **MCP Client**:Connects to the MCP server to retrieve available tools and invoke them as needed
   - **Google GenAI Integration**:Employs Google's Gemini model to process user inputs and determine appropriate tool invocations
   - **Interactive CLI**:Provides a command-line interface for user interaction, maintaining a chat history for context

---

### 🔧 Setup Instructions

To set up and run the project:

1. **Environment Configuration**:
    Ensure you have Node.js installe.
    Set up environment variables for the Twitter API credentials and Google Gemini API ke.

    ```plaintext
    GEMINI_API_KEY=...
    TWITTER_API_KEY=...
    TWITTER_API_SECRET=...
    TWITTER_ACCESS_TOKEN=...
    TWITTER_ACCESS_TOKEN_SECRET=...
    ```

2. **Dependency Installation**:
    Install necessary packages for both server and client applications using a package manager like np.

3. **Running the Server**:
    Start the Express server to listen for incoming SSE connections and handle tool invocation.

4. **Running the Client**:
    Launch the client application, which will connect to the MCP server and initiate the interactive CL.

5. **Interacting with the System**:
    Use the CLI to input queries. The AI model will process the input, decide if a tool invocation is necessary, and respond accordingl.

### Run the server
```bash
npm run dev
```

### Run the client 
```bash
node client.js
```