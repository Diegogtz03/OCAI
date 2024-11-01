"use client";

import { useState, useRef, useEffect } from "react";
import { Message, ChatResponse } from "@/interfaces/messages";
import { HistoryList } from "@/components/HistoryList/HistoryList";
import { ExampleCarrousel } from "@/components/ExampleCarrousel/ExampleCarrousel";
import { Menu } from "../svg/menu";
import { NewIcon } from "../svg/new";

export const ChatBox = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatId, setChatId] = useState<string>("");
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    // If messages are empty, request a new chat and save ID to cookies or something
    e.preventDefault();
    if (message.trim() === "") return;
    const message_to_send = message;

    setMessage("");

    setMessages((prevMessages) => [
      ...prevMessages,
      {
        id: Date.now().toString(),
        content: message_to_send,
        role: "user",
        createdAt: new Date(),
      },
    ]);

    setTimeout(async () => {
      setIsLoading(true);

      const response = await fetch("/api/chat", {
        method: "POST",
        body: JSON.stringify({
          newChat: messages.length == 0,
          message: message_to_send,
          email: "diego_gtz_t@hotmail.com",
          chatId: chatId,
        }),
      });

      const data: ChatResponse = await response.json();

      if (messages.length == 0) {
        // Save chat ID to cookies or something
        // Cookies.set("chatId", data.chatId);
        setChatId(data.chatId);
      }

      console.log(data);

      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now().toString(),
          content: data.message.content,
          role: data.message.role,
          createdAt: new Date(),
        },
      ]);

      setIsLoading(false);
    }, 500); // 500 milliseconds delay
  };

  const handleNewChat = () => {
    // ASK if sure to leave, if so, clear ID and reset chat
    if (messages.length == 0) return;
    setMessages([]);
  };

  return (
    <div className="flex flex-row items-center justify-center relative">
      {/* History List */}
      <div
        className={`flex flex-col w-fit h-full text-center border-gray-300 border-[1px] rounded-md p-4 shadow-sm min-w-[15rem] max-w-[15rem] min-h-[35rem] max-h-[35rem] absolute left-0 top-0 transition-transform duration-300 ease-in-out z-10 ${
          isHistoryOpen ? "-translate-x-full" : "translate-x-0"
        }`}
      >
        <HistoryList />
      </div>

      {/* Chat */}
      <div className="flex flex-col w-fit text-center border-gray-300 border-[1px] rounded-md p-4 shadow-sm min-w-[35rem] max-w-[35rem] min-h-[35rem] max-h-[35rem] z-20 bg-white h-full">
        {/* Top Bar */}
        <div className="flex justify-between items-center mb-2">
          <button
            className="flex items-center gap-2 bg-gray-200 p-2 rounded-md active:bg-gray-300"
            onClick={() => setIsHistoryOpen(!isHistoryOpen)}
          >
            <Menu />
          </button>

          <button
            className="flex items-center gap-2 bg-gray-200 p-2 rounded-md active:bg-gray-300"
            onClick={handleNewChat}
          >
            <NewIcon />
          </button>
        </div>

        {/* Chat messages */}
        <div className="flex-1 flex-col overflow-scroll p-4 space-y-4 border-[1px] border-gray-300 rounded-md flex end-1">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex break-words first:mt-auto ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[70%] p-2 rounded-lg text-left ${
                  message.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-black"
                }`}
              >
                <p>{message.content}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start items-center max-w-[70%] h-fit w-fit p-3 rounded-lg bg-gray-200 text-black">
              <div id="wave" className="flex gap-1 h-full">
                <span className="bg-gray-400 rounded-full w-2 h-2 animate-wave"></span>
                <span className="bg-gray-400 rounded-full w-2 h-2 animation-delay-300 animate-wave"></span>
                <span className="bg-gray-400 rounded-full w-2 h-2 animation-delay-600 animate-wave"></span>
              </div>
            </div>
          )}

          {messages.length == 0 && (
            <div className="flex first:mt-auto">
              <ExampleCarrousel />
            </div>
          )}

          <div ref={messagesEndRef} />
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
    </div>
  );
};
