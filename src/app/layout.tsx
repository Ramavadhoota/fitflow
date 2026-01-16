'use client';

import { ReactNode } from 'react';
import Navigation from '@/components/Navigation';
import '../globals.css';

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>FitFlow - AI Fitness Platform</title>
        <meta name="description" content="Multi-agent AI fitness platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <Navigation />
        {children}
      </body>
    </html>
  );
}
