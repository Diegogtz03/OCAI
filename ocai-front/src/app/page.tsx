import { redirect } from "next/navigation";
import { getServerSession } from "next-auth";
import { ChatBox } from "@/components/ChatBox/ChatBox";

export default async function Home() {
  const session = await getServerSession();

  if (!session || !session.user) {
    redirect("/auth");
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <div className="z-10 w-full max-w-4xl p-5 flex items-center justify-center font-mono text-sm">
        <ChatBox />
      </div>
    </main>
  );
}
