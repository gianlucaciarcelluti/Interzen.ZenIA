package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class HistoricIdentityLinkDTO {
	String type;
    String userId;
    String groupId;
    String taskId;
    String processInstanceId;
    String scopeId;
    String subScopeId;
    String scopeType;
    String scopeDefinitionId;
    LocalDateTime createTime;
}
