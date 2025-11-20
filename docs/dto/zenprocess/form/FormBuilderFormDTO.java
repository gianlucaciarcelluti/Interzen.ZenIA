package it.interzen.zencommonlibrary.dto.zenprocess.form;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class FormBuilderFormDTO extends TrackBasicChangesDTO implements HasID<Long> {
    Long id;
    String[] processDefinitionKeys;
    String[] processDefinitionNames;
    String formKey;
    String formName;
    String formJson;
    WebFormCompleteModeEnum formCompleteMode = WebFormCompleteModeEnum.SINGLE;
}
