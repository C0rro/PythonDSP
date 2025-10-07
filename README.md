# DSP Audio Raspberry Pi

Un **DSP audio in tempo reale** per Raspberry Pi, progettato per correggere acusticamente impianti audio professionali tramite filtri IIR calcolati con **REW**.

---

## Funzionalità principali

- Lettura e scrittura audio in tempo reale con **PyAudio**.  
- Applicazione di filtri **IIR di secondo ordine** calcolati a partire dalle misure acustiche.  
- Buffer configurabile per gestione latenza.  
- **Interfaccia web con Flask** per:
  - Selezione dei dispositivi audio di input/output.  
  - Scelta del file dei filtri.  
  - Modalità **Pass-Through** o **Filtrato**.  
- Elaborazione audio in **thread separato**, garantendo controllo in tempo reale senza blocchi.

---

## Requisiti

- Raspberry Pi (o qualsiasi computer Linux/Mac/Windows per test)  
- Python 3.10+  
- Librerie Python:

```bash
pip install numpy pyaudio flask
```


## Come configuarare il programma

1. **Misurazione della risposta in frequenza**  
   - Utilizzare REW per acquisire la risposta acustica del proprio impianto audio.

2. **Calcolo dei filtri**  
   - Sempre tramite REW, calcolare i filtri necessari per correggere la risposta.

3. **Esportazione dei coefficienti**  
   - Esportare i filtri in un file di testo.  
   - Il formato è simile a quello dei MiniDSP (`b0, b1, b2, a1, a2`)

4. **Posizionamento del file**  
   - Inserire il file dei filtri nella cartella **`Filtri/`** del progetto.

5. **Avvio dell’applicazione**  
   - Aprire il terminale nella cartella del progetto e lanciare:
   ```bash
   python main.py
   
6. **Configurazione e controllo tramite web**  
   - Aprire un browser e navigare su: http://indirizo_ip_del_dispositivo:5000
   - Selezionare i dispositivi audio di input e output  
   - Scegliere il file dei filtri dalla cartella `Filtri/`  
   - Impostare il buffer size (chunk) e il sample rate desiderati  
   - Premere **Avvia** per iniziare lo stream audio  
   - Nella pagina di controllo, selezionare:
     - **Pass-Through**: audio diretto senza filtraggio  
     - **Filtrato**: applica i filtri IIR calcolati da REW  
   - Premere **Stop** per terminare lo stream in sicurezza



