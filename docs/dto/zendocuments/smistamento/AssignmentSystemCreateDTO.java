package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.zenprotocollo.ProtocolDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentSystemCreateDTO {
	private Long id;
	private String title;
	private String notes;
	private Long documentId;
	
	//--- Campi da protocollo
	private Long protocolId;
	private Long companyId;
	private Long aooId;
	private LocalDateTime expireDate;
	private String protocolSearchData;
	
	private ProtocolDTO protocol;
	private LookupElementDTOLong<?> aoo;

	//--- Campi per smistamento
	private List<AssigneeCreateDTO> assignees = new ArrayList<>();

	private Long protocolledBy;
}