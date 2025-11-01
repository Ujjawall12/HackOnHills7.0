# HackOnHills7.0 - Manhattan Project

## Overview

Manhattan is a comprehensive data sanitization and secure erasure platform designed for various storage device types. The project provides both web and application interfaces for secure data erasure methods compliant with NIST SP 800-88 standards.

## Project Structure

```
Manhattan/
├── web-manhattan/          # Web-based interface (React + TypeScript)
├── app-manhattan/          # Application components
├── media-control-files/    # Media control utilities
└── readme/                 # Documentation
```

## Web Manhattan (`web-manhattan`)

A modern web application built with React, TypeScript, and shadcn-ui components for secure data erasure operations.

### Features

- **Multi-Device Support**: Self-Encrypting Drives (SEDs), SATA SSDs, NVMe SSDs, and Traditional HDDs
- **NIST Compliant**: All methods follow NIST SP 800-88 guidelines
- **User-Friendly Interface**: Modern UI built with shadcn-ui components
- **Comparison Tools**: Compare different erasure methods side-by-side
- **Reference Documentation**: Built-in documentation and guidelines

### Supported Erasure Methods

1. **Self-Encrypting Drives (SEDs)**
   - Cryptographic Erasure via MEK destruction
   - NIST SP 800-88: Purge

2. **SATA SSDs (Non-SED)**
   - ATA Secure Erase (Enhanced)
   - NIST SP 800-88: Purge

3. **NVMe SSDs**
   - NVMe Sanitize
   - NIST SP 800-88: Purge

4. **Traditional HDDs**
   - ATA Secure Erase
   - NIST SP 800-88: Purge

### Getting Started

#### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

#### Installation

```bash
cd Manhattan/web-manhattan
npm install
```

#### Development

```bash
npm run dev
```

The application will start on `http://localhost:5173`

#### Build

```bash
npm run build
```

## Technologies

- **Vite** - Next-generation frontend tooling
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **shadcn-ui** - High-quality component library
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide React** - Icon library

## Contributing

This project was created for HackOnHills7.0. Contributions and improvements are welcome!

## License

MIT License

## Repository

[GitHub Repository](https://github.com/Ujjawall12/HackOnHills7.0)

