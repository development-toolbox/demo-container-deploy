# demo-container-deploy - Dokumentation

### **Översikt**
Det här projektet använder **Terraform** för att skapa en **Podman-container** som kör en **Reveal.js-presentation** baserad på Markdown. CI/CD är integrerat för Terraform-validering, linting och säkerhetsskanning av containern med **Trivy**.

---

## **Kom igång**

### **1. Klona projektet**
```bash
git clone https://github.com/development-toolbox/demo-container-deploy.git
cd demo-container-deploy
```

### **2. Initiera Terraform**
```bash
terraform init
```

### **3. Starta containern**
```bash
terraform apply
```

### **4. Öppna presentationen**
- Gå till: **http://localhost:8000**

---

## **Projektstruktur**

```plaintext
terraform-revealjs/
├── .github/workflows/   # CI/CD pipelines
│   ├── terraform-ci.yml        # Terraform CI/CD
│   └── revealjs-trivy.yml      # Reveal.js och säkerhetsskanning
├── .tflint.hcl          # TFLint-konfiguration
├── Dockerfile           # Docker-konfiguration för Reveal.js
├── main.tf              # Terraform-konfiguration
├── presentation.md      # Markdown för presentationen
├── start.sh             # Startskript för Reveal.js-server
├── theme.css            # Anpassat tema för presentationen
```

---

## **CI/CD Pipelines**

| **Pipeline**        | **Beskrivning**                                   |
|---------------------|--------------------------------------------------|
| **Terraform CI/CD** | Validerar, lintar och planerar Terraform-koden.  |
| **Reveal.js CI/CD** | Bygger och skannar Docker-image med Trivy.       |

---

## **Uppdatera Presentationen**

1. Redigera filen `presentation.md` för att ändra innehållet.
2. Applicera ändringar:
   ```bash
   terraform apply
   ```
3. Ladda om webbläsaren.

---

## **Felsökning**

- **Port 8000 används redan?**
  ```bash
  sudo fuser -k 8000/tcp
  ```

- **Terraform-fel?**
  - Kontrollera planen:
    ```bash
    terraform plan
    ```

- **Container startar inte?**
  ```bash
  podman ps -a  # Kontrollera containerstatus
  podman logs revealjs-container  # Visa loggar
  ```

---

## **Avinstallera**

Ta bort alla resurser:
```bash
terraform destroy
```

---

Slim och enkel dokumentation, perfekt för snabb referens. Behöver du fler detaljer eller någon ytterligare sektion?