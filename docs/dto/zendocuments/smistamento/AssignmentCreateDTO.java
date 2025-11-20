package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import java.util.List;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentCreateDTO implements HasID<Long>{
	//TODO: Tutto recuperato dal documentId a cascata?
	private Long id;
	
	//private String title;
	//private String notes;
	private Long documentId;
	//private Long protocolId;
	//private Long companyId;
	//private Long aooId;
	
	
	//private List<AssignmentCorrespondentCreateDTO> correspondents;
}
