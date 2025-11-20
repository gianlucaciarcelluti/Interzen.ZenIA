package it.interzen.zencommonlibrary.dto.zendocuments;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import jakarta.persistence.Column;
import jakarta.validation.constraints.NotNull;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class ModelDTO extends TrackBasicChangesDTO implements HasID<Long>, LookupEntityGReturnLongPK<ModelDTO> {
	private Long id;
	
	@NotNull
	String code;
	
	@NotNull
	private String name;
	
	private String description;		

	@NotNull
	Boolean active = true;
	
	// Elenco dei metadati associati
	List<ModelMetadataDTO> metadata;

	// Tipo del modello
	private ModelTypeEnum modelType;

	private LookupElementDTOLong<FolderDTO> folderId;

	private String digitalArchiveProfileCode;
	
	// riferimento al registro particolare di ZenProtocollo
    private String registryCode;

	private List<ModelConfigurationDTO> configuration;

	public ModelDTO() {
		
	}
	
	ModelDTO(String code) {
		this.code = code;
	}

	@JsonIgnore
	@Override
	public LookupElementDTOLong<ModelDTO> getLookupElementDTOLong() {
		return new LookupElementDTOLong<>(getId(), getName(), getCode());
	}
}
