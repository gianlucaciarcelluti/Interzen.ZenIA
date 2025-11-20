package it.interzen.zencommonlibrary.dto.zenmaster;

import io.quantics.multitenant.tenantdetails.TenantDatabaseDetails;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class TenantDTO implements TenantDatabaseDetails {

    private String id;

    private String name;

    private String cognome;

    private String email;

    private String ragioneSociale;

    private String hostdb;

    private String portdb;

    private String database;

    private String userdb;

    private String pwdb;

    private String issuer;

    private String partner;

    private String storageAccountContainerName;
    
    private String storageAccountConnectionString;

    private Boolean tenantMaintenance;

    @Override
    public String getJwkSetUrl() {
        return this.issuer + "/protocol/openid-connect/certs";
    }


    public TenantDTO(AddTenantRequestDTO in){
        this.id = in.getId();
        this.name = in.getName();
        this.cognome = in.getCognome();
        this.email = in.getEmail();
        this.ragioneSociale = in.getRagioneSociale();
        this.hostdb = in.getHostdb();
        this.portdb = in.getPortdb();
        this.database = in.getDatabase();
        this.userdb = in.getUserdb();
        this.pwdb = in.getPwdb();
        this.issuer = in.getIssuer();
    }

}