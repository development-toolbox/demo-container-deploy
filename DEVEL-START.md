
## **Demo av container deploy första draften av demot**

### **Struktur**

```
terraform-revealjs/
├── .github/
│   └── workflows/
│       ├── terraform-ci.yml          # CI/CD för Terraform
│       └── revealjs-trivy.yml        # CI/CD för Reveal.js och Trivy
├── .tflint.hcl                       # TFLint-konfiguration
├── Dockerfile                        # Dockerfile för Reveal.js-container
├── main.tf                           # Terraform-konfiguration för Podman
├── presentation.md                   # Markdown-fil för Reveal.js presentation
├── start.sh                          # Startskript för Reveal.js
├── theme.css                         # Anpassat tema för Reveal.js
```

---

### **1. `main.tf`** (Terraform-konfiguration)

```hcl
provider "podman" {
  uri = "unix:///run/user/$(id -u)/podman/podman.sock"
}

resource "podman_image" "revealjs" {
  name   = "revealjs"
  source = "./Dockerfile"
}

resource "podman_container" "revealjs_presentation" {
  image = podman_image.revealjs.id
  name  = "revealjs-container"

  ports {
    external = 8000
    internal = 8000
  }

  volumes = [
    "${path.module}/presentation.md:/app/presentation.md",
    "${path.module}/theme.css:/app/reveal.js/css/theme/custom.css"
  ]

  command = ["sh", "-c", "/app/start.sh"]
}
```

---

### **2. `Dockerfile`**

```dockerfile
FROM node:16-alpine

# Installera Reveal.js och nödvändiga verktyg
WORKDIR /app
RUN apk add --no-cache git && \
    git clone https://github.com/hakimel/reveal.js.git && \
    cd reveal.js && \
    npm install && \
    npm install -D markdown

# Kopiera startskript
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Exponera port
EXPOSE 8000

CMD ["/app/start.sh"]
```

---

### **3. `presentation.md`** (Markdown-presentation)

```markdown
# Välkommen till Reveal.js!

---

## Sektion 1

- Punkt 1
- Punkt 2
- Punkt 3

---

## Sektion 2

```python
print("Hello, World!")
```

---

## Tack!
```

---

### **4. `theme.css`** (Anpassat Tema)

```css
/* Anpassat Reveal.js-tema */
.reveal {
  background-color: #f0f0f0;
}

.reveal .slides section {
  color: #333;
  font-family: "Arial", sans-serif;
}
```

---

### **5. `start.sh`** (Startskript)

```bash
#!/bin/sh
cd /app/reveal.js
# Dynamiskt stöd för presentation och teman
npx serve --port 8000 --single --content ../presentation.md --theme custom
```

---

### **6. `.tflint.hcl`** (TFLint-konfiguration)

```hcl
# Globala inställningar för TFLint
config {
  ignore_module = false
}

# Aktivera regler för att validera Terraform-standarder
rule "terraform_required_providers" {
  enabled = true
}

rule "terraform_deprecated_interpolation" {
  enabled = true
}
```

---

### **7. CI/CD för Terraform (`terraform-ci.yml`)**

```yaml
name: Terraform CI/CD

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.5

      - name: Install TFLint
        run: |
          curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
          sudo mv tflint /usr/local/bin/

      - name: Run TFLint
        run: tflint

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan
```

---

### **8. CI/CD för Reveal.js och Trivy (`revealjs-trivy.yml`)**

```yaml
name: Reveal.js CI/CD

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build-and-scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Build Docker Image
        run: |
          docker build -t revealjs:latest .

      - name: Install Trivy
        run: |
          wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.45.0_Linux-64bit.tar.gz
          tar zxvf trivy_0.45.0_Linux-64bit.tar.gz
          sudo mv trivy /usr/local/bin/

      - name: Scan Dockerfile
        run: trivy config .

      - name: Scan Docker Image
        run: trivy image --severity HIGH --exit-code 1 revealjs:latest
```

---

### **Så här kör du projektet:**

1. **Initiera Terraform**:
   - Kör kommandot för att initiera Terraform:
   ```bash
   terraform init
   ```

2. **Applicera Terraform**:
   - Kör Terraform och skapa Podman-containern:
   ```bash
   terraform apply
   ```

3. **Starta Presentationen**:
   - Gå till `http://localhost:8000` för att se din Reveal.js-presentation.

4. **GitHub Actions CI/CD**:
   - När du pushar till `main` eller öppnar en pull request, kommer GitHub Actions att köra pipelines för Terraform, Trivy-skanning och TFLint.

---

### **Förväntat Flöde:**

1. **CI/CD för Terraform**:
   - Validerar och planerar Terraform-konfigurationen.
2. **CI/CD för Reveal.js och Trivy**:
   - Bygger Dockerbilden och skannar den för sårbarheter.
3. **TFLint**:
   - Kontrollerar Terraform-koden för potentiella fel och standardbrott.

