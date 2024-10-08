"use client";

import Image from "next/image";
import { signIn, useSession } from "next-auth/react";
import { redirect } from "next/navigation";
import localFont from "next/font/local";

const oracleFont = localFont({
  src: "../../../public/fonts/OracleSans_ULt.ttf",
  weight: "400",
});

export default function Signup() {
  const { data: session } = useSession();

  if (session) {
    redirect("/");
  }

  const handleSignInGithub = async (providerId: string) => {
    const result = await signIn(providerId, {
      callbackUrl: "/",
      redirect: false,
      windowFeatures: "width=800,height=600",
    });

    if (result?.url) {
      window.open(result.url, "GitHubLogin", "width=800,height=600");
    }

    if (result?.error) {
      console.error("Authentication failed:", result.error);
    }
  };

  const handleSignInGoogle = async (providerId: string) => {
    const result = await signIn(providerId, {
      callbackUrl: "/",
      redirect: false,
      windowFeatures: "width=800,height=600",
    });

    if (result?.url) {
      window.open(result.url, "GoogleLogin", "width=800,height=600");
    }

    if (result?.error) {
      console.error("Authentication failed:", result.error);
    }
  };

  return (
    <main className="bg-backgroundLight dark:bg-backgroundDark">
      <div className="mx-auto flex h-screen max-w-6xl flex-wrap content-center justify-center px-6 text-gray-600">
        <div className=" flex flex-col items-center">
          <div className="space-y-15 flex flex-col items-center justify-center rounded-[25px] bg-gray-100 p-8">
            <div className="flex flex-col items-center justify-center space-y-4">
              <h1 className={`text-3xl ${oracleFont.className}`}>Sign In</h1>
            </div>
            <div className="mt-10 flex flex-col items-center justify-center space-y-4">
              <button
                className="flex h-12 w-64 items-center justify-center rounded-lg border-2 border-[#0000001a] bg-[#24292f] px-4 py-3 text-lg text-white transition ease-in-out hover:bg-[#24292fcc]"
                id="provider-button-github"
                onClick={() => handleSignInGithub("github")}
              >
                <Image
                  loading="lazy"
                  height="24"
                  width="24"
                  id="provider-logo-dark"
                  src="https://authjs.dev/img/providers/github.svg"
                  alt="Github Logo"
                ></Image>
                <span className="grow">Sign in with GitHub</span>
              </button>
              <button
                className="flex h-12 w-64 items-center justify-center rounded-lg border-2 border-[#0000001a] bg-white px-4 py-3 text-lg text-black transition ease-in-out hover:bg-[#ffffffcc]"
                onClick={() => handleSignInGoogle("google")}
              >
                <Image
                  loading="lazy"
                  height="24"
                  width="24"
                  id="provider-logo-dark"
                  src="https://authjs.dev/img/providers/google.svg"
                  alt="Google Logo"
                ></Image>
                <span className={`grow`}>Sign in with Google</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
