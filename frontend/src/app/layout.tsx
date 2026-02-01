import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geist = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TaskFlow - Professional Task Management",
  description: "A modern, secure, and lightning-fast task management application. Organize your tasks efficiently with TaskFlow.",
  applicationName: "TaskFlow",
  authors: [{ name: "TaskFlow" }],
  generator: "Next.js",
  keywords: ["todo", "task management", "productivity", "organize"],
  metadataBase: new URL("http://localhost:3000"),
  viewport: {
    width: "device-width",
    initialScale: 1,
    maximumScale: 5,
    userScalable: true,
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon.svg", type: "image/svg+xml" },
    ],
    apple: [{ url: "/logo.svg", type: "image/svg+xml" }],
  },
  manifest: "/manifest.json",
  themeColor: "#0B0F0E",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "TaskFlow",
  },
  formatDetection: {
    telephone: false,
  },
  openGraph: {
    type: "website",
    url: "http://localhost:3000",
    title: "TaskFlow - Professional Task Management",
    description: "A modern, secure, and lightning-fast task management application.",
    images: [
      {
        url: "/logo.svg",
        width: 200,
        height: 200,
        alt: "TaskFlow Logo",
      },
    ],
  },
  twitter: {
    card: "summary",
    title: "TaskFlow - Professional Task Management",
    description: "Organize your tasks efficiently with TaskFlow.",
    images: ["/logo.svg"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* Favicon - Primary .ico format (universally supported) */}
        <link rel="icon" href="/favicon.ico?v=1" type="image/x-icon" />
        {/* Fallback SVG favicon for modern browsers */}
        <link rel="icon" href="/favicon.svg?v=1" type="image/svg+xml" />

        {/* Apple Touch Icon for iOS */}
        <link rel="apple-touch-icon" href="/logo.svg" />

        {/* Web App Manifest */}
        <link rel="manifest" href="/manifest.json" />

        {/* Theme Color */}
        <meta name="theme-color" content="#0B0F0E" />
        <meta name="msapplication-TileColor" content="#0B0F0E" />

        {/* Additional Meta Tags */}
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="TaskFlow" />
      </head>
      <body className={`${geist.variable} ${geistMono.variable} antialiased bg-[#0B0F0E] text-[#E6F2EF]`}>
        {children}
      </body>
    </html>
  );
}
