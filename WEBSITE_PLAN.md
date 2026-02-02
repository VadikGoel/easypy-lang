# Website Generation Guide (v0.dev + GitHub Pages)

## Step 1: Generate the Site with v0.dev
Go to [v0.dev](https://v0.dev) and paste this prompt to get a professional documentation site for Easypy:

> **Prompt for v0:**
> "Create a modern, dark-themed landing page and documentation site for a new programming language called 'Easypy'. 
> The design should be sleek, like Next.js or Rust documentation.
> 
> **Key Sections:**
> 1. **Hero:** Title 'Easypy', Tagline 'The Easiest Language for Everyone'. Buttons: 'Get Started' and 'Download v2.0'.
> 2. **Features Grid:** 
>    - 🚀 **Native Performance**: Transpiles to raw Python.
>    - 📦 **Package Manager**: Built-in 'epi' tool installs any PyPI package.
>    - 🖥️ **Real GUI**: Create native windows with 3 lines of code.
>    - 🛠️ **VS Code Support**: Syntax highlighting extension included.
> 3. **Code Comparison:** Show a side-by-side comparison.
>    *Left (Easypy):* `use gui; app = gui.create_app("Hello", 300, 200); gui.show(app)`
>    *Right (Python):* Show the complex Tkinter boilerplate.
> 4. **Installation:** `git clone repo` then `.\easypy.bat file.ep`.
> 
> Use a color palette of Emerald Green, Dark Slate, and White."

## Step 2: Download & Install
1. When v0 generates the perfect design, click the **"Code"** button (top right).
2. Choose **"React"** or **"HTML"**. (HTML is easier for GitHub Pages if you don't want a build step).
3. If you choose HTML/Tailwind:
   - Download the `index.html` file.
   - Place it inside the `docs/` folder in this workspace.

## Step 3: Publish to GitHub Pages
1. Push your code to GitHub.
2. Go to Repository **Settings** -> **Pages**.
3. Under "Build and deployment", select **Source: Deploy from a branch**.
4. Select components: **Branch: main** (or master) and **Folder: /docs**.
5. Click Save.

Your site will be live at `https://<your-username>.github.io/<repo-name>/`!
