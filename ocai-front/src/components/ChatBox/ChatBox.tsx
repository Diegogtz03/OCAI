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
    <div className="w-fit text-center border-gray-300 border-[1px] rounded-md p-4 shadow-sm min-w-[35rem] min-h-[35rem] max-h-[35rem] relative">
      <div className="w-full h-full text-center">
        {/* CHAT INTERACTION */}
        <div className="flex flex-col space-y-2 overflow-y-auto h-full">
          {messages.map((message) => (
            <div key={message.id} className="flex justify-start">
              {message.role === "user" ? (
                <div className="flex justify-end">
                  <p>{message.content}</p>
                </div>
              ) : (
                <div className="flex justify-start">
                  <p>{message.content}</p>
                </div>
              )}
            </div>
          ))}
        </div>
        <form
          className="flex justify-center items-center space-x-2 absolute bottom-5 w-full"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            value={message}
            className="w-full p-2 border border-gray-300 rounded-md max-w-[400px]"
            placeholder="Talk to OCAI"
            onChange={(e) => setMessage(e.target.value)}
          />
          <button className="bg-blue-500 text-white p-2 rounded-md">
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
