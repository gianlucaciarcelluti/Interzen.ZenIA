package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SpecialRegisterFolderMappingDTO extends TrackBasicChangesDTO implements HasID<Long> {
    private Long id;
	
	private Long aooid;
	
    private String registryCode;
    
	private Long folderid;
}
