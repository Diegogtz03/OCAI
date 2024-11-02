import Image from "next/image";

export const Footer = () => {
  return (
    <div className="fixed bottom-0 left-0 w-screen h-96 rounded-t-lg">
      <Image
        src="/oracle_bottom_texture.png"
        className="absolute left-0 top-0 rounded-lg"
        alt="footer"
        fill={true}
      />
    </div>
  );
};
