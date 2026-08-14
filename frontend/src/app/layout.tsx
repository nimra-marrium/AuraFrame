import "./globals.css";

export const metadata = {
  title: "AuraFrame",
  description: "Turn scattered inspiration into structured creative direction.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
