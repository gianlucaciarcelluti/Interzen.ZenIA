package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SchemaTemplateOutDTO implements HasID<Long>{
	
	private Long id;
	private String description;
	private String extendedDescription;
	private String pathDescription;
	private ClassificationSchemaNodeType nodeType;
	private int depth;
	private int numbering;
	private String numberingPath;
	private String numberingLabel;
	private Long parentNode = null;
	private Long templateNode = null;
	private Boolean inactive;
	private List<Long> aoo = new ArrayList<>();
	private Long folderId = null;
	
}
