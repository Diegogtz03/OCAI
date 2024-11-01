// post route
export async function POST(req: Request) {
  const {
    newChat,
    email,
    message,
    chatId,
  }: { newChat: boolean; email: string; message: string; chatId: string } =
    await req.json();

  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ newChat, email, message, chatId }),
  });

  const data = await response.json();

  return Response.json(data);
}
