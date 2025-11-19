# Custom NiFi Extensions

Questa directory contiene estensioni personalizzate per Apache NiFi in formato NAR (NiFi Archive).

## 📦 Estensioni Disponibili

Attualmente non ci sono estensioni custom. I Process Groups utilizzano i processor standard di NiFi:

- **InvokeHTTP**: chiamate REST API
- **ExecuteScript**: logica custom (Python/Groq)
- **RouteOnAttribute**: routing condizionale
- **EvaluateJsonPath**: parsing JSON
- **PutDatabaseRecord**: salvataggio PostgreSQL
- **UpdateAttribute**: manipolazione metadata

## 🔧 Come Creare Custom Processor

Se in futuro servisse un processor personalizzato:

### 1. Setup Progetto Maven

```bash
git clone https://github.com/apache/nifi.git
cd nifi
mvn clean install -DskipTests

# Crea nuovo processor
cd nifi-nar-bundles
mkdir nifi-custom-bundle
cd nifi-custom-bundle

# Usa archetype
mvn archetype:generate \
  -DarchetypeGroupId=org.apache.nifi \
  -DarchetypeArtifactId=nifi-processor-bundle-archetype
```

### 2. Implementa Processor

```java
package com.interzen.nifi.processors;

@Tags({"groq", "llm", "generation"})
@CapabilityDescription("Genera documento con Groq API")
public class GroqGeneratorProcessor extends AbstractProcessor {
    
    @Override
    public void onTrigger(ProcessContext context, ProcessSession session) {
        FlowFile flowFile = session.get();
        if (flowFile == null) return;
        
        // Leggi input
        String metadata = session.read(flowFile, in -> 
            IOUtils.toString(in, StandardCharsets.UTF_8)
        );
        
        // Chiama Groq API
        String generated = callGroqAPI(metadata);
        
        // Scrivi output
        flowFile = session.write(flowFile, out -> 
            out.write(generated.getBytes(StandardCharsets.UTF_8))
        );
        
        session.transfer(flowFile, REL_SUCCESS);
    }
}
```

### 3. Build NAR

```bash
mvn clean package
```

Output: `target/nifi-custom-nar-1.0.0.nar`

### 4. Deploy

```bash
# Copia NAR in questa directory
cp target/nifi-custom-nar-1.0.0.nar \
   infrastructure/nifi-workflows/nifi-extensions/

# Riavvia NiFi
docker-compose restart nifi
```

## 📚 Documentazione

- [NiFi Developer Guide](https://nifi.apache.org/developer-guide.html)
- [Custom Processor Tutorial](https://nifi.apache.org/docs/nifi-docs/html/developer-guide.html#custom-processors)

## ⚠️ Note

Al momento non sono necessarie estensioni custom. I processor standard coprono tutte le esigenze:

- **SP01**: InvokeHTTP + ExecuteScript (Python)
- **SP02**: RouteOnAttribute + ExecuteScript
- **SP05**: InvokeHTTP (LanguageTool API) + ExecuteScript
- **SP08**: UpdateAttribute + PutDatabaseRecord

Creare custom processor solo se:
- Logica molto complessa non esprimibile in script
- Performance critiche (script più lento)
- Riutilizzo in molti flow
