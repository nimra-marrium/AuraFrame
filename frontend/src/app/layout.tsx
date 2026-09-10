import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";

export const metadata = {
  title: "AuraFrame",
  description: "Turn scattered inspiration into structured creative direction.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}