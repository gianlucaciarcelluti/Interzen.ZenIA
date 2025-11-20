package it.interzen.zencommonlibrary.dto.zenadmin;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import lombok.Data;

@Data
public class ProtAOODTO extends TableLookupEntityDTOGLongPK<ProtAOODTO> implements LookupEntityGReturnLongPK<ProtAOODTO> {
	private String managerName;
	private String managerSurname;
	private String managerFiscalCode;
	private String digitalPreservationManagerName;
	private String digitalPreservationManagerSurname;
	private String digitalPreservationManagerFiscalCode;
	private LookupElementDTOLong<CompanyDTO> companyId;
	private java.util.Date establishmentdate;
	private java.util.Date suppressiondate;
	private Boolean inviaNotificaProtocollazione;
}