"use client";

import { useState } from "react";
import { Message } from "@/interfaces/messages";

export const ChatBox = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(message);
    setMessage("");
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        id: Date.now().toString(),
        content: message,
        role: "user",
        createdAt: new Date(),
      },
    ]);

    setIsLoading(true);

    // Add demo response with a delay
    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now().toString(),
          content: "Hello, how can I help you?",
          role: "assistant",
          createdAt: new Date(),
        },
      ]);
      setIsLoading(false);
    }, 500); // 500 milliseconds delay
  };

  return (
    <div className="flex flex-col w-fit text-center border-gray-300 border-[1px] rounded-md p-4 shadow-sm min-w-[35rem] max-w-[35rem] min-h-[35rem] max-h-[35rem]">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 border-[1px] border-gray-300 rounded-md flex flex-col justify-end">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[70%] p-2 rounded-lg ${
                message.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-black"
              }`}
            >
              <p>{message.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Chat input */}
      <div className="p-4">
        <form className="flex items-center space-x-2" onSubmit={handleSubmit}>
          <input
            type="text"
            value={message}
            className="flex-1 p-2 border border-gray-300 rounded-md"
            placeholder="Talk to OCAI"
            onChange={(e) => setMessage(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white p-2 rounded-md"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

{
  /* 
  Features:
    - Start a new chat (back and forth)
    - View previous chats (history list, with dates, select to view more)
*/
}
