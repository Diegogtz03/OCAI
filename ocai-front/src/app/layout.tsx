import type { Metadata } from "next";
import SessionProvider from "@/components/SessionProvider"
import { getServerSession } from "next-auth"

import "./globals.css";

export const metadata: Metadata = {
  title: "OCAI",
  description: "MadHacks 2024",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getServerSession()

  return (
    <html lang="en">
      <body
        className={`antialiased`}
      >
        <SessionProvider session={session}>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
