# 🎯 Product Vision: Nugi Content Factory

## 1. Executive Summary
**Nugi Content Factory** adalah sistem produksi konten pemasaran berbasis AI (*AI Content Production System*) yang dirancang khusus untuk memproduksi materi promosi berkonversi tinggi, konsisten, dan scalable bagi industri properti.

## 2. Core Problem Statement
Dalam industri properti (Developer, Principal Agen, Sales Manager):
- Pembuatan materi promosi harian sering terhambat antrean tim desain grafis.
- Menggunakan generator AI biasa sering menghasilkan teks gambar yang cacat (typo, teks acak/halusinasi) dan layout visual yang tidak konsisten dengan panduan brand.
- Konten edukasi dan penawaran leads iklan sering kali lambat diproduksi sehingga kehilangan momentum pasar.

## 3. Product Principles
1. **LLM as Reasoning Engine:** Model bahasa besar (LLM) digunakan semata-mata untuk riset angle, hook, copywriting, dan visual prompting — **BUKAN** sebagai renderer visual.
2. **AI Image Models for Backgrounds Only:** Model generasi visual seperti Flux hanya menghasilkan canvas/latar belakang visual berkualitas tinggi, tanpa teks atau logo.
3. **Deterministic Rendering:** Tipografi judul, badge kategori, padding, kontras, dan penempatan logo dirender secara pasti (*pixel-perfect & deterministic*) menggunakan Python Pillow / SVG.
4. **Provider Abstraction:** Semua provider AI (LLM, Image Gen, Storage) menggunakan interface terisolasi sehingga mudah diganti atau diuji tanpa biaya API.
5. **No-CLI Desktop Target:** Dirancang sejak hari pertama agar pada versi rilis dapat dibundel menjadi aplikasi desktop Windows (`Setup.exe`) tanpa mewajibkan user memahami command line, Python, Node, atau Docker.

## 4. Target Audience
* **Primary (Phase 1):** NugiProperti internal team untuk memproduksi konten edukasi, tips follow-up leads, dan materi promosi perumahan/rukost.
* **Secondary (Future):** Kantor agen properti, pengembang perumahan, dan pengelola aset properti sebagai custom marketing automation client tool.
