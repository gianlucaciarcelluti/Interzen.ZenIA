package it.interzen.zencommonlibrary.dto.zenmaster;

import java.util.Date;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@ToString
public class AddTenantRequestDTO {

    private String id;
    private String name;
    private String hostdb;
    private String portdb;
    private String database;
    private String userdb;
    private String pwdb;
    private String issuer;
    private String ragioneSociale;
    private StatoTenant statoTenant;
    private String cognome;
    private String email;
    private Date creationDate;
    private String createdBy;
    private Date modificationDate;
    private String modifiedBy;
    private Date deletionDate;
    private String deletedBy;
    private Boolean inactive;

    public enum StatoTenant {
        Attivare, Attivato, Disattivato, Cancellato
    }
    
}
