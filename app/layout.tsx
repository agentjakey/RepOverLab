import type { Metadata } from "next";
import { Sora, Lora, DM_Mono } from "next/font/google";
import "./globals.css";

const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  display: "swap",
});

const lora = Lora({
  subsets: ["latin"],
  variable: "--font-lora",
  display: "swap",
});

const dmMono = DM_Mono({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-dm-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Representation Overlap Lab",
  description:
    "An interactive visual essay about why safety boundaries are not always cleanly separable in embedding space.",
  openGraph: {
    title: "Representation Overlap Lab",
    description: "Why safety boundaries are not always cleanly separable.",
    type: "article",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Representation Overlap Lab",
    description: "Why safety boundaries are not always cleanly separable.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${sora.variable} ${lora.variable} ${dmMono.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
