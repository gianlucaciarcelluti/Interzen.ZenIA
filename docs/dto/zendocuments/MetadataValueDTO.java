package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.Data;

import java.util.List;

@Data
public class MetadataValueDTO {
	String metadataCode;
	String label;

	@Enumerated(EnumType.STRING)
    MetadataDefTypeEnum type;

	String value;
	List<LookupDTO> lookupValues;
}
