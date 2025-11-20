package it.interzen.zencommonlibrary.dto.zenadmin;

import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;

/**
 * @author Gianluca Lella
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserDTO extends TrackBasicChangesDTOHasID<Long> {
    private Long id;
    private String externalid;
    private String username;
    private String name;
    private String surname;
    private String email;
    private String timezone = "(GMT+1:00) Europe/Rome";
    private String fiscalcode;
    private UtenteTrackBasicChangesDTO managerid;
    private String language= "IT";
    private String password;
    private Boolean active =true;
    private Boolean emailVerified =true;
    private AdminLookupDTO role;
    private ArrayList<RequireActions> requiredActions = new ArrayList<>();
    private Boolean temporaryPassword = false;

}