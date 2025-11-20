package it.interzen.zencommonlibrary.dto.zenmaster;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LicenzaAttivaFiltrataDTO {
    private Long id;
    private String descrizione;
    private String microservizi;
    private Long numero_accessi;
    private Date dataDecorrenza;
    private Date dataScadenza;
    private Integer tipoAccessi;
    private Integer quotaDisco;
    private Integer numeroDocumenti;
    private Integer numeroRagioniSociali;

}
