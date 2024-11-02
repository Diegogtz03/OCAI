"use client";

import { signOut } from "next-auth/react";
import localFont from "next/font/local";

const oracleFont = localFont({
  src: "../../../public/fonts/OracleSans_ULt.ttf",
  weight: "400",
});

export const SignOutButton = () => {
  return (
    <button
      className={`z-20 text-sm bg-gray-300 flex items-center rounded-md p-4 border-black border-[1px] cursor-pointer ${oracleFont.className}`}
      onClick={() => signOut()}
    >
      Sign out
    </button>
  );
};
