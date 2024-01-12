import os
import socket
import sys
import pefile
import math

IMPORT_BLACK_LIST = "UnhookWindowsHookEx,GetMessage,RegisterHotKey,SetWindowsHookEx,FindWindowA,ShowWindow,GetSystemDirectoryA,WideCharToMultiByte,CreateProcessA,Accept,AdjustTokenPrivileges,AttachThreadInput,Bind,BitBlt,CertOpenSystemStore,Connect,ConnectNamedPipe,ControlService,CreateFile,CreateFileMapping,CreateMutex,CreateProcess,CreateRemoteThread,CreateService,CreateToolhelp32Snapshot,CryptAcquireContext,DeviceIoControl,EnableExecuteProtectionSupport,EnumProcesses,EnumProcessModules,FindFirstFile,FindNextFile,FindResource,FindWindow,FtpPutFile,GetAdaptersInfo,GetAsyncKeyState,SelectObject,CreateCompatibleBitmap,CreateCompatibleDC,GetWindowDC,GetDC,GetForegroundWindow,Gethostbyname,Gethostname,GetKeyState,GetModuleFilename,GetModuleHandle,GetProcAddress,GetStartupInfo,GetSystemDefaultLangId,GetTempPath,GetThreadContext,GetVersionEx,GetWindowsDirectory,inet_addr,InternetOpen,InternetOpenUrl,InternetReadFile,InternetWriteFile,WriteFile,IsDebuggerPresent,CheckRemoteDebuggerPresent,OutputDebugStringA,OutputDebugStringW,URLDownloadToFile,WinExec,ShellExecute,OpenProcess,VirtualAllocEx,WriteProcessMemory,CreateRemoteThread,FindResource,LoadResource,SizeOfResource,SetFileAttributesW,SetConsoleMode,RegOpenKeyExW,RegQueryValueA,GetModuleHandleA,GetModuleFileNameA,CloseHandle,RtlUnwind,GetLastError,GetACP,GetEnviromentStrings".split(',')

class PE_DATASET :
	def __init__(self,filepath) :
		self.pe = pefile.PE(filepath)

	def get_num_of_suspicious_import_func(self) :
		TEMP_LIST = []
		for importeddll in self.pe.DIRECTORY_ENTRY_IMPORT :
			for importedapi in importeddll.imports :
				a = bytes.decode(importedapi.name)
				if type(importedapi) != 'NoneType' :
					TEMP_LIST.append(a)
		#print(TEMP_LIST)
		return len([l for l in IMPORT_BLACK_LIST if l in TEMP_LIST])

	def has_embeded_pefile(self) :
		txt = self.pe.get_memory_mapped_image()
		n = txt.count(str.encode('This program cannot be run in DOS mode.'))
		return 0 if n==1 else n

	def get_entropy(self) :
		data = self.pe.__data__.read(self.pe.__data__.size())
		data = str(data)
		entropy = 0
		size = self.pe.__data__.size()
		for x in range(256) :
			p_x = float(data.count(chr(x))/size)
			if p_x > 0 :
				entropy += - p_x * math.log(p_x, 2)
		return entropy