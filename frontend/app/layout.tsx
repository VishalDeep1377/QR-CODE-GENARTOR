import type { Metadata } from "next";
import "./globals.css";
import { Shell } from "@/components/shell";
export const metadata: Metadata = { title: "QR Studio — Create with intention", description: "A refined workspace to create, scan and manage QR codes." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body><Shell>{children}</Shell></body></html>; }
