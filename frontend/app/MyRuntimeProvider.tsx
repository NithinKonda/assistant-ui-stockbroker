"use client";

import { useRef } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useLangGraphRuntime } from "@assistant-ui/react-langgraph";
import { createThread, sendMessage } from "@/lib/chatApi";

export function MyRuntimeProvider({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const threadIdRef = useRef<string | undefined>();
  const runtime = useLangGraphRuntime({
    threadId: threadIdRef.current,
    stream: async (messages) => {
      if (!threadIdRef.current) {
        const { thread_id } = await createThread();
        console.log("Thread created with ID:", thread_id); // Debugging log
        threadIdRef.current = thread_id;
      }
  
      const threadId = threadIdRef.current;
      const response = await sendMessage({
        threadId,
        messages,
      });
  
      const newStreamedData = [];
      for await (const chunk of response) {
        console.log("Streaming data:", chunk); // Logs each chunk of streamed data
        newStreamedData.push(chunk.data);
      }
  
      console.log("Received data:", newStreamedData); // Logs the complete streamed data array
      return response;
    },
  });
  
  
  

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
    </AssistantRuntimeProvider>
  );
}
