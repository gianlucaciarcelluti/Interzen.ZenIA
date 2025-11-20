package it.interzen.zencommonlibrary.dto;

import java.util.List;

import it.interzen.zencommonlibrary.basedb.*;
import jakarta.annotation.PostConstruct;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import org.modelmapper.Converter;
import org.modelmapper.ModelMapper;
import org.modelmapper.PropertyMap;
import org.modelmapper.TypeMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor;
import org.springframework.beans.factory.annotation.Lookup;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.request.RequestContextHolder;

import it.interzen.zencommonlibrary.crud_base.CrudException;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.utility.CollectionUtilities;
import it.interzen.zencommonlibrary.utility.Couple;
import it.interzen.zencommonlibrary.utility.CurrentUserData;
import it.interzen.zencommonlibrary.utility.ThreadLocalAutoClear;
import lombok.Getter;
import lombok.Setter;

@Configuration
public class MapperConfigurationBase {
	@Autowired
	@Getter
	@Setter
	protected ModelMapper mapper;

	@Autowired
	@Getter
	@Setter
	protected ApplicationContext context;

	//ThreadLocalAutoClear<GetUserDTOFromMSAAdmin> msaAdmin = new ThreadLocalAutoClear<>(GetUserDTOFromMSAAdmin.class);

	@PersistenceContext
	protected EntityManager em;

	protected GetUserDTOFromMSAAdmin dataForNonSpringEnvironmentUser;
	protected GetGroupDTOFromMSAAdmin dataForNonSpringEnvironmentGroup;
	protected GetCompanyDTOFromMSAAdmin dataForNonSpringEnvironmentCompany;
	protected GetProtAOODTOFromMSAAdmin dataForNonSpringEnvironmentProtAOO;

	protected ThreadLocalAutoClear<GetUserDTOFromMSAAdmin> dataForNonWebUsageUser = new ThreadLocalAutoClear<>("returnGetUserDTOFromMSAAdminPrototype");
	protected ThreadLocalAutoClear<GetGroupDTOFromMSAAdmin> dataForNonWebUsageGroup = new ThreadLocalAutoClear<>("returnGetGroupDTOFromMSAAdminPrototype");
	protected ThreadLocalAutoClear<GetCompanyDTOFromMSAAdmin> dataForNonWebUsageCompany = new ThreadLocalAutoClear<>("returnGetCompanyDTOFromMSAAdminPrototype");
	protected ThreadLocalAutoClear<GetProtAOODTOFromMSAAdmin> dataForNonWebUsageProtAOO = new ThreadLocalAutoClear<>("returnGetProtAOODTOFromMSAAdminPrototype");

	@PostConstruct
	public void postConstruct() {
		//msaAdmin.setApplicationContext(context);
		dataForNonWebUsageUser.setApplicationContext(context);
		dataForNonWebUsageGroup.setApplicationContext(context);
		dataForNonWebUsageCompany.setApplicationContext(context);
		dataForNonWebUsageProtAOO.setApplicationContext(context);
	}

	@Lookup
	public GetUserDTOFromMSAAdmin getMSAAdminUser_lowLevel() {
		return dataForNonSpringEnvironmentUser;
	}

	@Lookup
	public GetGroupDTOFromMSAAdmin getMSAAdminGroup_lowLevel() {
		return dataForNonSpringEnvironmentGroup;
	}

	@Lookup
	public GetCompanyDTOFromMSAAdmin getMSAAdminCompany_lowLevel() {
		return dataForNonSpringEnvironmentCompany;
	}

	@Lookup
	public GetProtAOODTOFromMSAAdmin getMSAAdminProtAOO_lowLevel() {
		return dataForNonSpringEnvironmentProtAOO;
	}


	public GetUserDTOFromMSAAdmin getMSAAdminUser() {
		AutowiredAnnotationBeanPostProcessor a;

		if (dataForNonSpringEnvironmentUser != null) {
			return dataForNonSpringEnvironmentUser;
		}
		else if (RequestContextHolder.getRequestAttributes() != null) {
			return getMSAAdminUser_lowLevel();
		}
		else {
			return dataForNonWebUsageUser.get();
		}
	}

	public GetGroupDTOFromMSAAdmin getMSAAdminGroup() {
		AutowiredAnnotationBeanPostProcessor a;

		if (dataForNonSpringEnvironmentGroup != null) {
			return dataForNonSpringEnvironmentGroup;
		}
		else if (RequestContextHolder.getRequestAttributes() != null) {
			return getMSAAdminGroup_lowLevel();
		}
		else {
			return dataForNonWebUsageGroup.get();
		}
	}

	public GetCompanyDTOFromMSAAdmin getMSAAdminCompany() {
		AutowiredAnnotationBeanPostProcessor a;

		if (dataForNonSpringEnvironmentCompany != null) {
			return dataForNonSpringEnvironmentCompany;
		}
		else if (RequestContextHolder.getRequestAttributes() != null) {
			return getMSAAdminCompany_lowLevel();
		}
		else {
			return dataForNonWebUsageCompany.get();
		}
	}

	public GetProtAOODTOFromMSAAdmin getMSAAdminProtAOO() {
		AutowiredAnnotationBeanPostProcessor a;

		if (dataForNonSpringEnvironmentProtAOO != null) {
			return dataForNonSpringEnvironmentProtAOO;
		}
		else if (RequestContextHolder.getRequestAttributes() != null) {
			return getMSAAdminProtAOO_lowLevel();
		}
		else {
			return dataForNonWebUsageProtAOO.get();
		}
	}

	public void setMSAAdminUser(GetUserDTOFromMSAAdmin data) {
		dataForNonSpringEnvironmentUser = data;
	}
	public void setMSAAdminCompany(GetCompanyDTOFromMSAAdmin data) {
		dataForNonSpringEnvironmentCompany = data;
	}
	public void setMSAAdminProtAOO(GetProtAOODTOFromMSAAdmin data) {
		dataForNonSpringEnvironmentProtAOO = data;
	}

	protected Converter<UtenteTrackBasicChangesDTO, String> fromUserTrackBasicChangesDTOUserIDFunc() {
		Converter<UtenteTrackBasicChangesDTO, String> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}
			var id = e.getId();
			return id.toString();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<GroupTrackBasicChangesDTO, String> fromGroupTrackBasicChangesDTOGroupIDFunc() {
		Converter<GroupTrackBasicChangesDTO, String> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}
			var id = e.getId();
			return id.toString();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<CompanyTrackBasicChangesDTO, String> fromCompanyTrackBasicChangesDTOCompanyIDFunc() {
		Converter<CompanyTrackBasicChangesDTO, String> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}
			var id = e.getId();
			return id.toString();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<ProtAOOTrackBasicChangesDTO, String> fromProtAOOTrackBasicChangesDTOProtAOOIDFunc() {
		Converter<ProtAOOTrackBasicChangesDTO, String> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}
			var id = e.getId();
			return id.toString();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<Long, UtenteTrackBasicChangesDTO> fromUtenteIDToUtenteTrackBasicChangesDTOFunc() {
		return fromUserIDToUserTrackBasicChangesDTOFunc();
	}

	protected Converter<Long, GroupTrackBasicChangesDTO> fromGruppoIDToGroupTrackBasicChangesDTOFunc() {
		return fromGroupIDToGroupTrackBasicChangesDTOFunc();
	}

	protected Converter<Long, CompanyTrackBasicChangesDTO> fromCompanyIDToCompanyTrackBasicChangesDTOFunc() {
		return fromCompanyIDToCompanyTrackBasicChangesDTOConverterFunc();
	}

	protected Converter<CompanyTrackBasicChangesDTO, Long> fromCompanyDTOToCompanyIDFunc() {
		return fromCompanyDTOToCompanyIDConverterFunc();
	}

	protected Converter<Long, ProtAOOTrackBasicChangesDTO> fromProtAOOIDToProtAOOTrackBasicChangesDTOFunc() {
		return fromProtAOOIDToProtAOOTrackBasicChangesDTOConverterFunc();
	}

	protected Converter<ProtAOOTrackBasicChangesDTO, Long> fromProtAOODTOToProtAOOIDFunc() {
		return fromProtAOODTOToProtAOOIDConverterFunc();
	}

	protected Converter<Long, UtenteTrackBasicChangesDTO> fromUtenteToUtenteIDTrackBasicChangesDTOFunc() {
		return fromUserIDToUserTrackBasicChangesDTOFunc();
	}

	protected Converter<Long, UtenteTrackBasicChangesDTO> fromUserIDToUserTrackBasicChangesDTOFunc() {
		Converter<Long, UtenteTrackBasicChangesDTO> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			var h = getMSAAdminUser().get(e);
			return h;
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<Long, GroupTrackBasicChangesDTO> fromGroupIDToGroupTrackBasicChangesDTOFunc() {
		Converter<Long, GroupTrackBasicChangesDTO> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			// Il gruppo -1 è il gruppo "Everyone"
			if (e == -1) {
				GroupTrackBasicChangesDTO everyOneGroup = new GroupTrackBasicChangesDTO();
				everyOneGroup.setId(-1L);
				everyOneGroup.setName("Everyone");
				everyOneGroup.setType("Generico");
				everyOneGroup.setDescription("Everyone");
				return everyOneGroup;
			}
			var h = getMSAAdminGroup().get(e);
			return h;
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<Long, UtenteTrackBasicChangesDTO> fromUserIDLongToUserTrackBasicChangesDTOFunc() {
		Converter<Long, UtenteTrackBasicChangesDTO> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			var h = getMSAAdminUser().get(e.toString());
			return h;
		};

		return fromBaseLookupEntityToObject;
	}


	protected Converter<Long, CompanyTrackBasicChangesDTO> fromCompanyIDToCompanyTrackBasicChangesDTOConverterFunc() {
		Converter<Long, CompanyTrackBasicChangesDTO> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			var h = getMSAAdminCompany().get(e);
			return h;
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<CompanyTrackBasicChangesDTO, Long> fromCompanyDTOToCompanyIDConverterFunc() {
		Converter<CompanyTrackBasicChangesDTO, Long> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			return e.getId();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<ProtAOOTrackBasicChangesDTO, Long> fromProtAOODTOToProtAOOIDConverterFunc() {
		Converter<ProtAOOTrackBasicChangesDTO, Long> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			return e.getId();
		};

		return fromBaseLookupEntityToObject;
	}

	protected Converter<Long, ProtAOOTrackBasicChangesDTO> fromProtAOOIDToProtAOOTrackBasicChangesDTOConverterFunc() {
		Converter<Long, ProtAOOTrackBasicChangesDTO> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}

			var h = getMSAAdminProtAOO().get(e);
			return h;
		};

		return fromBaseLookupEntityToObject;
	}

	protected<T extends HasID<Long>> Converter<LookupElementDTOLong<T>, T> returnConvertedForBaseLookupElementDTO(Class<T> cl, String oggettoMessaggio) {
		Converter<LookupElementDTOLong<T>, T> fromBaseLookupEntityToObject = contextLocal -> {
			var e = contextLocal.getSource();
			if (e == null) {
				return null;
			}
			var id = e.getId();
			if (id == null) {
				return null;
			}

			var data = em.getReference(cl, id);
	    	/*
	    	var data = em.find(cl, id);
			if (data == null) {
				var s = String.format("%s non trovato per id:%d", oggettoMessaggio, id);
				throw new CrudException(s);
			}
			*/
			return data;
		};

		return fromBaseLookupEntityToObject;
	}

	protected<T> Converter<Long, T> returnConvertedForHasIDLong(Class<T> cl, String oggettoMessaggio) {
		Converter<Long, T> fromIDToObject = contextLocal -> {
			var id = contextLocal.getSource();
			if (id == null) {
				return null;
			}
			var data = em.find(cl, id);
			if (data == null) {
				var s = String.format("%s non trovato per id:%d", oggettoMessaggio, id);
				throw new CrudException(s);
			}

			return data;
		};

		return fromIDToObject;
	}

	public <T extends Enum<T>> Converter<List<String>, List<T>> returnConverterStringListToEnumList(Class<T> e) {
		Converter<List<String>, List<T>> fromIDToObject = contextLocal -> {
			var data = contextLocal.getSource();
			var result = CollectionUtilities.fromStringListToEnumList(data, e);

			return result;
		};

		return fromIDToObject;
	}

	public <T> Converter<List<T>, List<T>> returnConverteCopyList(Class<T> cl) {
		Converter<List<T>, List<T>> fromIDToObject = contextLocal -> {
			var data = contextLocal.getSource();
			var result = CollectionUtilities.copyList(data);

			return result;
		};

		return fromIDToObject;
	}

	public <T extends Enum<T>> Converter<List<T>, List<String>> returnConverterEnumListToStringList(Class<T> e) {
		Converter<List<T>, List<String>> fromIDToObject = contextLocal -> {
			var data = contextLocal.getSource();
			var result = CollectionUtilities.fromEnumListToStringList(data, e);

			return result;
		};

		return fromIDToObject;
	}

	public<T extends TrackBasicChangesI & HasID<Long>, TDTO extends TrackBasicChangesDTOHasLongID>
	Couple<TypeMap<T, TDTO>, TypeMap<TDTO, T>> mapperBaseLookupEntityDTO(Class<T> clT, Class<TDTO> clTDO)
	{
		TypeMap<T, TDTO> propertyMapperAOOToDTO = this.mapper.createTypeMap(clT, clTDO);

		TypeMap<TDTO, T> propertyMapperDTOToBaseLookupEntity =
				mapper.addMappings(new PropertyMap<TDTO, T>() {
					@Override
					protected void configure() {
						skip(destination.getCreatedBy());
						skip(destination.getCreationDate());
						skip(destination.getModifiedBy());
						skip(destination.getModificationDate());
					}
				});

		Converter<Long, T> fromIDToObject = context -> {
			var id = context.getSource();
			if (id == null) {
				return null;
			}
			var data = em.find(clT, id);
			if (data == null) {
				throw new CrudException("Lookup non trovata " + id);
			}

			return data;
		};

		// i dati si prendono dal DB
		propertyMapperDTOToBaseLookupEntity.addMappings(
				mapperLocal -> {
					var temp2 = mapperLocal.using(fromIDToObject);
					temp2.map(HasID::getId, TrackBasicChangesI::setTrackingBasicChangesValueFromDB);
				}
		);

		return new Couple<>(propertyMapperAOOToDTO, propertyMapperDTOToBaseLookupEntity);
	}

	public CurrentUserData getCurrentUserData() {
		return CurrentUserData.getCurrentUserDataFromContext(context);
	}
}
