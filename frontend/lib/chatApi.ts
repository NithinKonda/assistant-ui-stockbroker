import { ThreadState, Client } from "@langchain/langgraph-sdk";
import { LangChainMessage } from "@assistant-ui/react-langgraph";

const createClient = () => {
  const apiUrl =
    process.env["NEXT_PUBLIC_LANGGRAPH_API_URL"] || 
    "http://127.0.0.1:5000"; // Fallback to local Python backend
  return new Client({
    apiUrl,
  });
};


export const createAssistant = async (graphId: string) => {
  const client = createClient();
  return client.assistants.create({ graphId });
};

export const createThread = async () => {
  try {
    const client = createClient();
    return await client.threads.create();
  } catch (error) {
    console.error("Error creating thread:", error);
    throw error; // Re-throw the error if needed
  }
};

export const getThreadState = async (
  threadId: string
): Promise<ThreadState<Record<string, any>>> => {
  const client = createClient();
  return client.threads.getState(threadId);
};

export const updateState = async (
  threadId: string,
  fields: {
    newState: Record<string, any>;
    asNode?: string;
  }
) => {
  const client = createClient();
  return client.threads.updateState(threadId, {
    values: fields.newState,
    asNode: fields.asNode!,
  });
};

export const sendMessage = async (params: {
  threadId: string;
  messages: LangChainMessage[];
}) => {
  try {
    const client = createClient();
    const input: Record<string, any> = { messages: params.messages };
    const config = {
      configurable: {
        model_name: "openai",
      },
    };
    return await client.runs.stream(
      params.threadId,
      process.env["NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID"]!,
      {
        input,
        config,
        streamMode: "messages",
      }
    );
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
};
