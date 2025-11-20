package it.interzen.zencommonlibrary.dto.zenprotocollo;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.basedb.Searchable;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CorrespondentOutDTO implements Searchable {

    @Schema(description="Identifies if this correspondent is a contact or a office/uor")
    private CorrespondentType correspondentType;
    private String id;
    private String name;
    private String officeCode;
    private String vatNumber;
    private String fiscalCode;
    private String pec;
    private String city;
    private String zipCode;
    private String address;
    private String email;
    private String firstname;
    private String lastname;


/*
    //PER CONTATTO O COMUNI
    private String id;
    private String name;
    private String legalStatus;
    //changed
    private List<String> contactType = new ArrayList<>();
    private String category;
    private String IPACode;
    private String AOOCode;
    private LookupElementDTOLong<?> countryId;
    private LookupElementDTOLong<?> districtId;
    private String city;
    private String zipCode;
    private String address;
    private String phone;
    private String fax;
    private String email;
    private String vatNumber;
    private String pec;
    private String fiscalCode;
    private String url;

    //PER OFFICE/UOR
    private String externalid;
    //changed
    private GruppoDTO.GruppoTipo officeType;
    private String officeCode;
    private LookupElementDTOLong<?> officeAOOID;
    private String officePhone;
    private String officeFax;
    private UtenteTrackBasicChangesDTO officeManager;
    private Integer parentOffice;
    private Boolean active;

    public CorrespondentOutDTO() {
        this.active =true;
    }
    */
    @Getter
    public enum CorrespondentType{
        CONTACT("Contact"),
        UOR("UOR");

        private final String testo;
        CorrespondentType(String testo) {
            this.testo = testo;
        }
        public String getTesto() {
            return testo;
        }
    }


	@Override
	public String createSearchString() {
        String nameSearch = "";
		if(firstname != null && lastname != null) {
            //Fix per ricerca su nome e cognome senza ordinamento es. "Fabio Rossi" == "Rossi Fabio
            nameSearch = firstname + " " + lastname + " " + firstname;
        }
        else{
            nameSearch = name;
        }


        return StringUtils.defaultString(nameSearch) + " " + StringUtils.defaultString(email)+ " " + StringUtils.defaultString(pec);
	}




}
