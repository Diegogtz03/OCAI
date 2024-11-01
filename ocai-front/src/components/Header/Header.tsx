import { SignOutButton } from "@/components/SignOutButton/SignOutButton";
import { getServerSession } from "next-auth";
import localFont from "next/font/local";
import Image from "next/image";

const oracleFont = localFont({
  src: "../../../public/fonts/OracleSans_ULt.ttf",
  weight: "400",
});

export const Header = async () => {
  const session = await getServerSession();

  return (
    <div className="fixed top-0 left-0 flex justify-end p-4 w-screen bg-gray-100 h-24 rounded-b-lg overflow-hidden">
      {session && (
        <div className="flex justify-end p-4">
          <SignOutButton />
        </div>
      )}
      <div className="mr-4 absolute left-5 flex items-center">
        <Image
          src="/oracle_logo.png"
          className="rounded-lg mr-4"
          alt="logo"
          width={60}
          height={60}
        />
        <div className={`text-3xl left-20 ${oracleFont.className}`}>OCAI</div>
      </div>
      <Image
        src="/oracle_texture.png"
        className="absolute right-0 bottom-0"
        alt="logo"
        width={100}
        height={100}
      />
    </div>
  );
};
