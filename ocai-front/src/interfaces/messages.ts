export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  createdAt: Date;
}

export interface ChatResponse {
  message: {
    role: "user" | "assistant";
    content: string;
  };
  chatId: string;
}
