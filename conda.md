# 🐍 Anaconda Environment Management — Quick Notes

* **Anaconda** → Full package (Python + conda + Jupyter + libraries)
* **conda** → Tool to manage packages & environments
* **Jupyter Notebook** → Interface to write and run code interactively 
```
jupyter notebook
or 
jupyter lab
```

👉 Simple: **Anaconda = bundle**, **conda = manager**, **Jupyter = workspace**

---

## 🔹 What is Anaconda?

* A Python distribution for:

  * Package management
  * Environment management
* Comes with tools like Jupyter and many pre-installed libraries

```
conda activate
anaconda-navigator
```

---

## 🔹 What is an Environment?

* A **self-contained folder** with:

  * Its own Python version
  * Its own packages
* Prevents conflicts between projects

---

## 🔹 Tool used: conda

* Manages:

  * Environments
  * Packages
  * Python versions

---

# ⚙️ Environment Commands

## 🆕 Create Environment

```bash
conda create --name myenv python=3.10
```

* Creates environment `myenv`
* Installs Python 3.10

---

## ▶️ Activate Environment

```bash
conda activate myenv
```

* Switch into the environment
* All installs now go inside it

---

## ⏹️ Deactivate Environment

```bash
conda deactivate
```

* Exit current environment

---

## 📦 Install Packages

```bash
conda install numpy pandas
```

* Installs packages in active environment

Optional (less preferred with conda):

```bash
pip install requests
```
---

## 📦 list Installed Packages

```bash
conda list
```

* to list all the installed packages in the current env

```bash
conda info --envs
```

* to check current environment
---

## 📋 List Environments

```bash
conda env list
```

* Shows all environments + their paths

---

## 🔁 Switch Environment

```bash
conda activate another_env
```

---

## ❌ Delete Environment

```bash
conda remove --name myenv --all
```

* Completely removes environment

---

# 📁 Where Environments Are Stored

## Default location:

```
anaconda3/envs/
```

### Example:

```
anaconda3/
└── envs/
    ├── myenv/
    ├── test-env/
```

* Each environment = a **folder**
* Contains full Python setup

---

## 🔍 Check Exact Path

```bash
conda env list
```

Example output:

```
myenv   /home/user/anaconda3/envs/myenv
```

---

## 📍 Custom Location (Optional)

```bash
conda create --prefix /path/to/env python=3.10
```

* Creates environment in a custom folder

---

# 🔄 Environment Sharing (Reproducibility)

## Export environment

```bash
conda env export > environment.yml
```

## Recreate environment

```bash
conda env create -f environment.yml
```

---

# 🧠 Key Takeaways

* Environment = **just a folder with isolated Python**
* Use environments for every project
* Always manage using `conda` (avoid manual edits)
* Helps avoid dependency conflicts

---